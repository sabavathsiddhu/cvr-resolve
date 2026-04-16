from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os, json, sys
from datetime import datetime
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
# In local development, it loads from .env. In production (Render/Vercel), 
# it will use the environment variables set in the dashboard.
load_dotenv() 
logger.info("Environment variables loaded")

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'cvr_resolve_secret_key_2024_supabase')
# Disable Werkzeug debugger to prevent exposing environment variables
app.config['PROPAGATE_EXCEPTIONS'] = True

# Supabase Database Configuration
# DATABASE_URL is the standard variable used by most platforms
DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL_POOLER = os.getenv('DATABASE_URL_POOLER')

# Use pooler if available (usually port 6543), otherwise use direct connection (port 5432)
ACTIVE_DATABASE_URL = DATABASE_URL_POOLER or DATABASE_URL

if not ACTIVE_DATABASE_URL:
    logger.error("FATAL: DATABASE_URL not found in environment!")
    # We don't raise ValueError immediately to allow the app to at least show a 500 page 
    # instead of crashing the whole container startup if possible, 
    # but for Gunicorn/Render, we should ensure it's logged.

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

BLOCKS = ['CM Block', 'Main Block', 'First Year Block', 'Library Block', 'Hostel Block', 'Labs Block', 'Sports Block', 'Canteen Block']

def get_db():
    """Get database connection from Supabase with enhanced error handling"""
    if not ACTIVE_DATABASE_URL:
        logger.error("❌ Database URL is not configured")
        return None
        
    try:
        # Ensure sslmode=require is present if not already in URL (Supabase requirement)
        db_url = ACTIVE_DATABASE_URL
        if "sslmode=" not in db_url:
            separator = "&" if "?" in db_url else "?"
            db_url += f"{separator}sslmode=require"
            
        logger.debug(f"Attempting database connection to: {db_url.split('@')[-1]}")
        conn = psycopg2.connect(db_url, connect_timeout=10)
        logger.info("✅ Database connected successfully")
        return conn
    except Exception as e:
        logger.error(f"❌ Database connection error: {type(e).__name__}: {str(e)}")
        # If it's a timeout or connection refused, it's likely a firewall/port issue
        if "timeout" in str(e).lower() or "refused" in str(e).lower():
            logger.error("HINT: This might be a firewall issue. Ensure you are using the Connection Pooler (port 6543) instead of direct connection (port 5432).")
        return None

def init_db():
    """Initialize database (tables already created by init_database.py)"""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class User(UserMixin):
    def __init__(self, id, username, role, name, email, assigned_blocks, pfp_path=None):
        self.id = id
        self.username = username
        self.role = role
        self.name = name
        self.email = email
        self.assigned_blocks = json.loads(assigned_blocks) if assigned_blocks else []
        self.pfp_path = pfp_path

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT * FROM users WHERE id=%s", (user_id,))
            u = c.fetchone()
            if u:
                return User(u['id'], u['username'], u['role'], u['name'], u['email'] or '', u['assigned_blocks'] or '[]', u.get('pfp_path'))
    except Exception as e:
        print(f"[ERROR] Loading user: {e}")
    finally:
        conn.close()
    
    return None

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash('Access denied.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return wrapper
    return decorator

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_duplicate(description, location, student_id):
    conn = get_db()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute(
                "SELECT id FROM complaints WHERE location=%s AND student_id!=%s AND status='Pending' AND LOWER(description) LIKE %s",
                (location, student_id, f'%{description[:20].lower()}%')
            )
            result = c.fetchone()
            return result['id'] if result else None
    finally:
        conn.close()

def assign_priority(description):
    high_keywords = ['broken', 'urgent', 'emergency', 'not working', 'damaged', 'leak', 'fire', 'danger']
    low_keywords = ['minor', 'small', 'suggest', 'request', 'paint']
    desc_lower = description.lower()
    if any(k in desc_lower for k in high_keywords): return 'High'
    if any(k in desc_lower for k in low_keywords): return 'Low'
    return 'Medium'

# ─── ROUTES ───

@app.route('/debug-db')
def debug_db():
    """Diagnostic route to check database connection and report errors"""
    status = {"connected": False, "error": None, "database_url_set": bool(ACTIVE_DATABASE_URL)}
    try:
        if not ACTIVE_DATABASE_URL:
            status["error"] = "DATABASE_URL environment variable is missing!"
            return jsonify(status), 500
            
        db_url = ACTIVE_DATABASE_URL
        if "sslmode=" not in db_url:
            separator = "&" if "?" in db_url else "?"
            db_url += f"{separator}sslmode=require"
            
        conn = psycopg2.connect(db_url, connect_timeout=5)
        with conn.cursor() as c:
            c.execute("SELECT 1")
            c.fetchone()
        conn.close()
        status["connected"] = True
        return jsonify(status)
    except Exception as e:
        status["error"] = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Debug DB Error: {status['error']}")
        return jsonify(status), 500

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        print(f"[LOGIN] Attempt for user: {username}", flush=True)
        logger.info(f"Login attempt for user: {username}")
        
        conn = get_db()
        if not conn:
            print("[LOGIN] Database connection failed", flush=True)
            logger.error("Database connection failed during login")
            flash('Database error. Try again later.', 'danger')
            return render_template('login.html')
        
        try:
            print(f"[LOGIN] Querying user: {username}", flush=True)
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, username))
                u = c.fetchone()
                print(f"[LOGIN] User found: {u is not None}", flush=True)
                logger.debug(f"User {username} found in DB: {u is not None}")
                
                if u and check_password_hash(u['password'], password):
                    print(f"[LOGIN] ✅ Login successful for {username}", flush=True)
                    logger.info(f"✅ Login successful for {username}")
                    user_obj = User(u['id'], u['username'], u['role'], u['name'], u['email'] or '', u['assigned_blocks'] or '[]')
                    login_user(user_obj)
                    return redirect(url_for('dashboard'))
                
                print(f"[LOGIN] Invalid credentials for {username}", flush=True)
                logger.warning(f"Failed login attempt for {username}")
                flash('Invalid credentials. Please try again.', 'danger')
        except Exception as e:
            print(f"[LOGIN] ❌ ERROR: {type(e).__name__}: {e}", flush=True)
            logger.error(f"Login error: {type(e).__name__}: {e}", exc_info=True)
            flash('An error occurred during login. Please try again later.', 'danger')
        finally:
            conn.close()
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'superadmin':
        return redirect(url_for('superadmin_dashboard'))
    elif current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('student_dashboard'))

# ─── STUDENT ───

@app.route('/student')
@login_required
@role_required('student')
def student_dashboard():
    logger.info(f"Student dashboard accessed by user: {current_user.username}")
    conn = get_db()
    if not conn:
        logger.error("Database connection failed for student dashboard")
        flash('Database error.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT * FROM complaints WHERE student_id=%s ORDER BY created_at DESC", (current_user.id,))
            complaints = c.fetchall() or []
            # Convert datetime to string for templates
            for comp in complaints:
                if comp['created_at']:
                    comp['created_at'] = comp['created_at'].isoformat()
                if comp['updated_at']:
                    comp['updated_at'] = comp['updated_at'].isoformat()
        
        logger.info(f"Retrieved {len(complaints)} complaints for student {current_user.username}")
        
        stats = {
            'total': len(complaints),
            'pending': sum(1 for c in complaints if c['status'] == 'Pending'),
            'completed': sum(1 for c in complaints if c['status'] == 'Completed')
        }
        return render_template('student_dashboard.html', complaints=complaints, stats=stats, blocks=BLOCKS)
    except Exception as e:
        logger.error(f"Student dashboard error: {type(e).__name__}: {e}", exc_info=True)
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))
    finally:
        conn.close()

@app.route('/student/complaint/new', methods=['GET', 'POST'])
@login_required
@role_required('student')
def new_complaint():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        
        if not title or not description or not location:
            flash('All fields required.', 'danger')
            return render_template('new_complaint.html', blocks=BLOCKS)
        
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = filename
        
        priority = assign_priority(description)
        dup_id = check_duplicate(description, location, current_user.id)
        
        conn = get_db()
        if not conn:
            flash('Database error.', 'danger')
            return render_template('new_complaint.html', blocks=BLOCKS)
        
        try:
            with conn.cursor() as c:
                c.execute(
                    "INSERT INTO complaints (student_id, title, description, image_path, location, status, priority, duplicate_of) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (current_user.id, title, description, image_path, location, 'Pending', priority, dup_id)
                )
                conn.commit()
            
            if dup_id:
                flash(f'Complaint submitted! Note: Similar complaint #{dup_id} exists.', 'warning')
            else:
                flash('Complaint submitted successfully!', 'success')
            return redirect(url_for('student_dashboard'))
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] New complaint: {e}")
            flash('Error submitting complaint.', 'danger')
        finally:
            conn.close()
    
    return render_template('new_complaint.html', blocks=BLOCKS)

@app.route('/student/complaint/<int:cid>')
@login_required
@role_required('student')
def view_complaint(cid):
    conn = get_db()
    if not conn:
        flash('Database error.', 'danger')
        return redirect(url_for('student_dashboard'))
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT * FROM complaints WHERE id=%s AND student_id=%s", (cid, current_user.id))
            complaint = c.fetchone()
        
        if not complaint:
            flash('Complaint not found.', 'danger')
            return redirect(url_for('student_dashboard'))
        
        return render_template('complaint_detail.html', complaint=complaint)
    finally:
        conn.close()

# ─── ADMIN ───

@app.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    conn = get_db()
    if not conn:
        flash('Database error.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        blocks = current_user.assigned_blocks
        block_filter = request.args.get('block', '')
        status_filter = request.args.get('status', '')
        search = request.args.get('search', '')
        
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            if blocks:
                placeholders = ','.join(['%s'] * len(blocks))
                query = f"SELECT c.*, u.name as student_name FROM complaints c JOIN users u ON c.student_id=u.id WHERE c.location IN ({placeholders})"
                params = list(blocks)
                
                if block_filter and block_filter in blocks:
                    query += " AND c.location=%s"
                    params.append(block_filter)
                if status_filter:
                    query += " AND c.status=%s"
                    params.append(status_filter)
                if search:
                    query += " AND (c.title ILIKE %s OR c.description ILIKE %s)"
                    params.extend([f'%{search}%', f'%{search}%'])
                
                query += " ORDER BY c.created_at DESC"
                c.execute(query, params)
                complaints = c.fetchall() or []
                # Convert datetime to string for templates
                for comp in complaints:
                    if comp['created_at']:
                        comp['created_at'] = comp['created_at'].isoformat()
                    if comp['updated_at']:
                        comp['updated_at'] = comp['updated_at'].isoformat()
            else:
                complaints = []
        
        stats = {
            'total': len(complaints),
            'pending': sum(1 for c in complaints if c['status'] == 'Pending'),
            'completed': sum(1 for c in complaints if c['status'] == 'Completed')
        }
        
        return render_template('admin_dashboard.html', complaints=complaints, stats=stats,
                             assigned_blocks=blocks, block_filter=block_filter,
                             status_filter=status_filter, search=search)
    finally:
        conn.close()

@app.route('/admin/complaint/<int:cid>/update', methods=['POST'])
@login_required
@role_required('admin')
def update_complaint(cid):
    conn = get_db()
    if not conn:
        flash('Database error.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT * FROM complaints WHERE id=%s", (cid,))
            complaint = c.fetchone()
        
        if not complaint or complaint['location'] not in current_user.assigned_blocks:
            flash('Access denied.', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        status = request.form.get('status')
        remarks = request.form.get('remarks', '')
        
        with conn.cursor() as c:
            c.execute(
                "UPDATE complaints SET status=%s, remarks=%s, updated_at=%s WHERE id=%s",
                (status, remarks, datetime.now(), cid)
            )
            conn.commit()
        
        flash('Complaint updated!', 'success')
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Update complaint: {e}")
        flash('Error updating complaint.', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('admin_dashboard'))

# ─── SUPER ADMIN ───

@app.route('/superadmin')
@login_required
@role_required('superadmin')
def superadmin_dashboard():
    conn = get_db()
    if not conn:
        flash('Database error.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        block_filter = request.args.get('block', '')
        status_filter = request.args.get('status', '')
        search = request.args.get('search', '')
        
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            query = "SELECT c.*, u.name as student_name FROM complaints c JOIN users u ON c.student_id=u.id WHERE 1=1"
            params = []
            
            if block_filter:
                query += " AND c.location=%s"
                params.append(block_filter)
            if status_filter:
                query += " AND c.status=%s"
                params.append(status_filter)
            if search:
                query += " AND (c.title ILIKE %s OR c.description ILIKE %s OR u.name ILIKE %s)"
                params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
            
            query += " ORDER BY c.created_at DESC"
            c.execute(query, params)
            complaints = c.fetchall() or []
            # Convert datetime to string for templates
            for comp in complaints:
                if comp['created_at']:
                    comp['created_at'] = comp['created_at'].isoformat()
                if comp['updated_at']:
                    comp['updated_at'] = comp['updated_at'].isoformat()
            
            c.execute("SELECT * FROM users WHERE role='admin' ORDER BY name")
            admins = c.fetchall() or []
            
            c.execute("SELECT location, COUNT(*) as cnt FROM complaints GROUP BY location")
            block_data = c.fetchall() or []
            c.execute("SELECT status, COUNT(*) as cnt FROM complaints GROUP BY status")
            status_data = c.fetchall() or []
            c.execute("SELECT priority, COUNT(*) as cnt FROM complaints GROUP BY priority")
            priority_data = c.fetchall() or []
        
        block_chart = {row['location']: row['cnt'] for row in block_data}
        # Add missing blocks with 0 count
        for block in BLOCKS:
            if block not in block_chart:
                block_chart[block] = 0
        # Sort by block name for consistent display
        block_chart = dict(sorted(block_chart.items()))
        status_chart = {row['status']: row['cnt'] for row in status_data}
        priority_chart = {row['priority']: row['cnt'] for row in priority_data}
        
        stats = {
            'total': len(complaints),
            'pending': sum(1 for c in complaints if c['status'] == 'Pending'),
            'completed': sum(1 for c in complaints if c['status'] == 'Completed'),
            'total_all': len(complaints)
        }
        
        return render_template('superadmin_dashboard.html', complaints=complaints, admins=admins,
                             stats=stats, blocks=BLOCKS, block_chart=json.dumps(block_chart),
                             status_chart=json.dumps(status_chart), priority_chart=json.dumps(priority_chart),
                             block_filter=block_filter, status_filter=status_filter, search=search)
    finally:
        conn.close()

@app.route('/superadmin/admin/new', methods=['POST'])
@login_required
@role_required('superadmin')
def create_admin():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    assigned_blocks = request.form.getlist('blocks')
    
    if not username or not password or not name:
        flash('All fields required.', 'danger')
        return redirect(url_for('superadmin_dashboard'))
    
    conn = get_db()
    if not conn:
        flash('Database error.', 'danger')
        return redirect(url_for('superadmin_dashboard'))
    
    try:
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO users (username, password, role, name, email, assigned_blocks) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, generate_password_hash(password), 'admin', name, email, json.dumps(assigned_blocks))
            )
            conn.commit()
        flash(f'Admin created!', 'success')
    except psycopg2.IntegrityError:
        conn.rollback()
        flash('Username already exists.', 'danger')
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Create admin: {e}")
        flash('Error creating admin.', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('superadmin_dashboard'))

@app.route('/superadmin/admin/<int:aid>/edit', methods=['POST'])
@login_required
@role_required('superadmin')
def edit_admin(aid):
    assigned_blocks = request.form.getlist('blocks')
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    
    conn = get_db()
    if not conn:
        flash('Database error.', 'danger')
        return redirect(url_for('superadmin_dashboard'))
    
    try:
        with conn.cursor() as c:
            c.execute(
                "UPDATE users SET name=%s, email=%s, assigned_blocks=%s WHERE id=%s AND role='admin'",
                (name, email, json.dumps(assigned_blocks), aid)
            )
            conn.commit()
        flash('Admin updated.', 'success')
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Edit admin: {e}")
        flash('Error updating admin.', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('superadmin_dashboard'))

@app.route('/superadmin/admin/<int:aid>/delete', methods=['POST'])
@login_required
@role_required('superadmin')
def delete_admin(aid):
    conn = get_db()
    if not conn:
        flash('Database error.', 'danger')
        return redirect(url_for('superadmin_dashboard'))
    
    try:
        with conn.cursor() as c:
            c.execute("DELETE FROM users WHERE id=%s AND role='admin'", (aid,))
            conn.commit()
        flash('Admin deleted.', 'success')
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Delete admin: {e}")
        flash('Error deleting admin.', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('superadmin_dashboard'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Handle password change
        current_pw = request.form.get('current_password')
        new_pw = request.form.get('new_password')
        
        conn = get_db()
        if not conn:
            flash('Database error.', 'danger')
            return redirect(url_for('profile'))
            
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("SELECT password FROM users WHERE id=%s", (current_user.id,))
                u = c.fetchone()
                
                if u and check_password_hash(u['password'], current_pw):
                    new_hash = generate_password_hash(new_pw)
                    with conn.cursor() as update_c:
                        update_c.execute("UPDATE users SET password=%s WHERE id=%s", (new_hash, current_user.id))
                        conn.commit()
                    flash('Password updated successfully!', 'success')
                else:
                    flash('Incorrect current password.', 'danger')
        finally:
            conn.close()
            
    return render_template('profile.html')

@app.route('/profile/picture', methods=['POST'])
@login_required
def upload_pfp():
    if 'pfp' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('profile'))
        
    file = request.files['pfp']
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(f"pfp_{current_user.id}_{int(datetime.now().timestamp())}.{file.filename.rsplit('.', 1)[1].lower()}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db()
        if conn:
            try:
                with conn.cursor() as c:
                    c.execute("UPDATE users SET pfp_path=%s WHERE id=%s", (filename, current_user.id))
                    conn.commit()
                flash('Profile picture updated!', 'success')
            finally:
                conn.close()
    
    return redirect(url_for('profile'))

@app.route('/superadmin/complaint/<int:cid>/update', methods=['POST'])
@login_required
@role_required('superadmin')
def superadmin_update_complaint(cid):
    status = request.form.get('status')
    remarks = request.form.get('remarks', '')
    
    conn = get_db()
    if not conn:
        flash('Database error.', 'danger')
        return redirect(url_for('superadmin_dashboard'))
    
    try:
        with conn.cursor() as c:
            c.execute(
                "UPDATE complaints SET status=%s, remarks=%s, updated_at=%s WHERE id=%s",
                (status, remarks, datetime.now(), cid)
            )
            conn.commit()
        flash('Complaint updated.', 'success')
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Update super admin complaint: {e}")
        flash('Error updating complaint.', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('superadmin_dashboard'))

@app.route('/superadmin/complaint/<int:cid>/delete', methods=['POST'])
@login_required
@role_required('superadmin')
def delete_complaint(cid):
    conn = get_db()
    if not conn:
        flash('Database error.', 'danger')
        return redirect(url_for('superadmin_dashboard'))
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT image_path FROM complaints WHERE id=%s", (cid,))
            complaint = c.fetchone()
        
        if complaint and complaint['image_path']:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], complaint['image_path']))
            except:
                pass
        
        with conn.cursor() as c:
            c.execute("DELETE FROM complaints WHERE id=%s", (cid,))
            conn.commit()
        flash('Complaint deleted.', 'success')
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Delete complaint: {e}")
        flash('Error deleting complaint.', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('superadmin_dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        
        if not username or not password or not name:
            flash('All fields required.', 'danger')
            return render_template('register.html')
        
        conn = get_db()
        if not conn:
            flash('Database error.', 'danger')
            return render_template('register.html')
        
        try:
            with conn.cursor() as c:
                c.execute(
                    "INSERT INTO users (username, password, role, name, email) VALUES (%s, %s, %s, %s, %s)",
                    (username, generate_password_hash(password), 'student', name, email)
                )
                conn.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            conn.rollback()
            flash('Username already exists.', 'danger')
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Register: {e}")
            flash('Registration error.', 'danger')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.template_filter('from_json')
def from_json_filter(s):
    try:
        return json.loads(s) if s else []
    except:
        return []

@app.template_filter('urlencode')
def urlencode_filter(s):
    from urllib.parse import quote_plus
    return quote_plus(str(s))

@app.errorhandler(500)
def handle_500(e):
    print(f"[500 ERROR] {type(e).__name__}: {e}", flush=True)
    logger.error(f"500 Error: {e}", exc_info=True)
    return "<h1>500 Error</h1><p>An internal server error occurred. Please try again later.</p>", 500

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"[EXCEPTION] {type(e).__name__}: {e}", flush=True)
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    return "<h1>Error</h1><p>An error occurred. Please try again later.</p>", 500

if __name__ == '__main__':
    init_db()
    # Use debug mode only in development (controlled by FLASK_ENV)
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('PORT', 5050))
    
    # Disable Werkzeug debugger in debug mode to prevent exposing sensitive data
    if debug_mode:
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port, use_debugger=False, use_reloader=False)
