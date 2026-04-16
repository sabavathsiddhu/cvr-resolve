from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3, os, json
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'cvr_resolve_secret_key_2024_professional'

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

BLOCKS = ['CM Block', 'Main Block', 'First Year Block', 'Library Block', 'Hostel Block', 'Labs Block', 'Sports Block', 'Canteen Block']

DB_PATH = os.path.join(app.root_path, 'instance', 'cvr.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        oauth_provider TEXT,
        oauth_id TEXT UNIQUE,
        role TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        assigned_blocks TEXT DEFAULT '[]',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        image_path TEXT,
        location TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        priority TEXT DEFAULT 'Medium',
        remarks TEXT,
        duplicate_of INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES users(id)
    )''')
    # Seed super admin
    existing = c.execute("SELECT id FROM users WHERE username='superadmin'").fetchone()
    if not existing:
        c.execute("INSERT INTO users (username, password, role, name, email) VALUES (?,?,?,?,?)",
            ('superadmin', generate_password_hash('super123'), 'superadmin', 'Super Admin', 'superadmin@cvr.ac.in'))
        # Seed block admins
        blocks_data = [
            ('cm_admin', 'admin123', 'admin', 'CM Block Admin', 'cm@cvr.ac.in', '["CM Block"]'),
            ('main_admin', 'admin123', 'admin', 'Main Block Admin', 'main@cvr.ac.in', '["Main Block"]'),
            ('fy_admin', 'admin123', 'admin', 'First Year Admin', 'fy@cvr.ac.in', '["First Year Block"]'),
            ('lab_admin', 'admin123', 'admin', 'Labs Admin', 'lab@cvr.ac.in', '["Labs Block","Library Block"]'),
        ]
        for u in blocks_data:
            c.execute("INSERT INTO users (username,password,role,name,email,assigned_blocks) VALUES (?,?,?,?,?,?)",
                (u[0], generate_password_hash(u[1]), u[2], u[3], u[4], u[5]))
        # Seed students
        students = [
            ('student1', 'stud123', 'student', 'Rahul Sharma', 'rahul@student.cvr.ac.in'),
            ('student2', 'stud123', 'student', 'Priya Reddy', 'priya@student.cvr.ac.in'),
        ]
        for s in students:
            c.execute("INSERT INTO users (username,password,role,name,email) VALUES (?,?,?,?,?)",
                (s[0], generate_password_hash(s[1]), s[2], s[3], s[4]))
        # Seed sample complaints
        sample_complaints = [
            (5, 'Broken AC', 'The AC in room 204 is not working since 3 days', None, 'CM Block', 'Pending', 'High'),
            (5, 'Water Leakage', 'Water leaking from ceiling near lab entrance', None, 'Labs Block', 'Pending', 'High'),
            (6, 'Broken Projector', 'Projector in seminar hall is damaged', None, 'Main Block', 'Completed', 'Medium'),
            (5, 'Wifi Not Working', 'WiFi in library reading room is down', None, 'Library Block', 'Pending', 'Medium'),
            (6, 'Broken Bench', 'Multiple benches broken in First Year classrooms', None, 'First Year Block', 'Pending', 'Low'),
        ]
        for comp in sample_complaints:
            c.execute("INSERT INTO complaints (student_id,title,description,image_path,location,status,priority) VALUES (?,?,?,?,?,?,?)", comp)
    conn.commit()
    conn.close()

class User(UserMixin):
    def __init__(self, id, username, role, name, email, assigned_blocks):
        self.id = id
        self.username = username
        self.role = role
        self.name = name
        self.email = email
        self.assigned_blocks = json.loads(assigned_blocks) if assigned_blocks else []

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    u = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    if u:
        return User(u['id'], u['username'], u['role'], u['name'], u['email'] or '', u['assigned_blocks'] or '[]')
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
    existing = conn.execute(
        "SELECT id FROM complaints WHERE location=? AND student_id!=? AND status='Pending' AND LOWER(description) LIKE ?",
        (location, student_id, f'%{description[:20].lower()}%')
    ).fetchone()
    conn.close()
    return existing['id'] if existing else None

def assign_priority(description):
    high_keywords = ['broken', 'urgent', 'emergency', 'not working', 'damaged', 'leak', 'fire', 'danger']
    low_keywords = ['minor', 'small', 'suggest', 'request', 'paint']
    desc_lower = description.lower()
    if any(k in desc_lower for k in high_keywords): return 'High'
    if any(k in desc_lower for k in low_keywords): return 'Low'
    return 'Medium'

# ─── ROUTES ───

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
        conn = get_db()
        u = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()
        if u and check_password_hash(u['password'], password):
            user_obj = User(u['id'], u['username'], u['role'], u['name'], u['email'] or '', u['assigned_blocks'] or '[]')
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials. Please try again.', 'danger')
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
    conn = get_db()
    complaints = conn.execute(
        "SELECT * FROM complaints WHERE student_id=? ORDER BY created_at DESC",
        (current_user.id,)
    ).fetchall()
    conn.close()
    stats = {'total': len(complaints), 'pending': sum(1 for c in complaints if c['status']=='Pending'),
             'completed': sum(1 for c in complaints if c['status']=='Completed')}
    return render_template('student_dashboard.html', complaints=complaints, stats=stats, blocks=BLOCKS)

@app.route('/student/complaint/new', methods=['GET', 'POST'])
@login_required
@role_required('student')
def new_complaint():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        if not title or not description or not location:
            flash('All fields are required.', 'danger')
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
        conn.execute(
            "INSERT INTO complaints (student_id,title,description,image_path,location,status,priority,duplicate_of) VALUES (?,?,?,?,?,?,?,?)",
            (current_user.id, title, description, image_path, location, 'Pending', priority, dup_id)
        )
        conn.commit()
        conn.close()
        if dup_id:
            flash(f'Complaint submitted! Note: A similar complaint (#{dup_id}) already exists.', 'warning')
        else:
            flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('student_dashboard'))
    return render_template('new_complaint.html', blocks=BLOCKS)

@app.route('/student/complaint/<int:cid>')
@login_required
@role_required('student')
def view_complaint(cid):
    conn = get_db()
    complaint = conn.execute("SELECT * FROM complaints WHERE id=? AND student_id=?", (cid, current_user.id)).fetchone()
    conn.close()
    if not complaint:
        flash('Complaint not found.', 'danger')
        return redirect(url_for('student_dashboard'))
    return render_template('complaint_detail.html', complaint=complaint)

# ─── ADMIN ───

@app.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    conn = get_db()
    blocks = current_user.assigned_blocks
    block_filter = request.args.get('block', '')
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '')
    query = "SELECT c.*, u.name as student_name FROM complaints c JOIN users u ON c.student_id=u.id WHERE c.location IN ({})".format(
        ','.join('?' for _ in blocks))
    params = list(blocks)
    if block_filter and block_filter in blocks:
        query += " AND c.location=?"
        params.append(block_filter)
    if status_filter:
        query += " AND c.status=?"
        params.append(status_filter)
    if search:
        query += " AND (c.title LIKE ? OR c.description LIKE ?)"
        params += [f'%{search}%', f'%{search}%']
    query += " ORDER BY c.created_at DESC"
    complaints = conn.execute(query, params).fetchall() if blocks else []
    stats = {'total': len(complaints), 'pending': sum(1 for c in complaints if c['status']=='Pending'),
             'completed': sum(1 for c in complaints if c['status']=='Completed')}
    conn.close()
    return render_template('admin_dashboard.html', complaints=complaints, stats=stats,
                           assigned_blocks=blocks, block_filter=block_filter,
                           status_filter=status_filter, search=search)

@app.route('/admin/complaint/<int:cid>/update', methods=['POST'])
@login_required
@role_required('admin')
def update_complaint(cid):
    conn = get_db()
    complaint = conn.execute("SELECT * FROM complaints WHERE id=?", (cid,)).fetchone()
    if not complaint or complaint['location'] not in current_user.assigned_blocks:
        flash('Access denied.', 'danger')
        conn.close()
        return redirect(url_for('admin_dashboard'))
    status = request.form.get('status')
    remarks = request.form.get('remarks', '')
    conn.execute("UPDATE complaints SET status=?, remarks=?, updated_at=? WHERE id=?",
                 (status, remarks, datetime.now(), cid))
    conn.commit()
    conn.close()
    flash('Complaint updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# ─── SUPER ADMIN ───

@app.route('/superadmin')
@login_required
@role_required('superadmin')
def superadmin_dashboard():
    conn = get_db()
    block_filter = request.args.get('block', '')
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '')
    query = "SELECT c.*, u.name as student_name FROM complaints c JOIN users u ON c.student_id=u.id WHERE 1=1"
    params = []
    if block_filter:
        query += " AND c.location=?"
        params.append(block_filter)
    if status_filter:
        query += " AND c.status=?"
        params.append(status_filter)
    if search:
        query += " AND (c.title LIKE ? OR c.description LIKE ? OR u.name LIKE ?)"
        params += [f'%{search}%', f'%{search}%', f'%{search}%']
    query += " ORDER BY c.created_at DESC"
    complaints = conn.execute(query, params).fetchall()
    admins = conn.execute("SELECT * FROM users WHERE role='admin' ORDER BY name").fetchall()
    # Analytics
    block_data = conn.execute("SELECT location, COUNT(*) as cnt FROM complaints GROUP BY location").fetchall()
    status_data = conn.execute("SELECT status, COUNT(*) as cnt FROM complaints GROUP BY status").fetchall()
    priority_data = conn.execute("SELECT priority, COUNT(*) as cnt FROM complaints GROUP BY priority").fetchall()
    total = conn.execute("SELECT COUNT(*) as cnt FROM complaints").fetchone()['cnt']
    conn.close()
    block_chart = {row['location']: row['cnt'] for row in block_data}
    status_chart = {row['status']: row['cnt'] for row in status_data}
    priority_chart = {row['priority']: row['cnt'] for row in priority_data}
    stats = {'total': len(complaints), 'pending': sum(1 for c in complaints if c['status']=='Pending'),
             'completed': sum(1 for c in complaints if c['status']=='Completed'),
             'total_all': total}
    return render_template('superadmin_dashboard.html', complaints=complaints, admins=admins,
                           stats=stats, blocks=BLOCKS, block_chart=json.dumps(block_chart),
                           status_chart=json.dumps(status_chart), priority_chart=json.dumps(priority_chart),
                           block_filter=block_filter, status_filter=status_filter, search=search)

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
    try:
        conn.execute("INSERT INTO users (username,password,role,name,email,assigned_blocks) VALUES (?,?,?,?,?,?)",
                     (username, generate_password_hash(password), 'admin', name, email, json.dumps(assigned_blocks)))
        conn.commit()
        flash(f'Admin "{name}" created successfully!', 'success')
    except sqlite3.IntegrityError:
        flash('Username already exists.', 'danger')
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
    conn.execute("UPDATE users SET name=?, email=?, assigned_blocks=? WHERE id=? AND role='admin'",
                 (name, email, json.dumps(assigned_blocks), aid))
    conn.commit()
    conn.close()
    flash('Admin updated.', 'success')
    return redirect(url_for('superadmin_dashboard'))

@app.route('/superadmin/admin/<int:aid>/delete', methods=['POST'])
@login_required
@role_required('superadmin')
def delete_admin(aid):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id=? AND role='admin'", (aid,))
    conn.commit()
    conn.close()
    flash('Admin deleted.', 'success')
    return redirect(url_for('superadmin_dashboard'))

@app.route('/superadmin/complaint/<int:cid>/update', methods=['POST'])
@login_required
@role_required('superadmin')
def superadmin_update_complaint(cid):
    status = request.form.get('status')
    remarks = request.form.get('remarks', '')
    conn = get_db()
    conn.execute("UPDATE complaints SET status=?, remarks=?, updated_at=? WHERE id=?",
                 (status, remarks, datetime.now(), cid))
    conn.commit()
    conn.close()
    flash('Complaint updated.', 'success')
    return redirect(url_for('superadmin_dashboard'))

@app.route('/superadmin/complaint/<int:cid>/delete', methods=['POST'])
@login_required
@role_required('superadmin')
def delete_complaint(cid):
    conn = get_db()
    c = conn.execute("SELECT image_path FROM complaints WHERE id=?", (cid,)).fetchone()
    if c and c['image_path']:
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], c['image_path']))
        except: pass
    conn.execute("DELETE FROM complaints WHERE id=?", (cid,))
    conn.commit()
    conn.close()
    flash('Complaint deleted.', 'success')
    return redirect(url_for('superadmin_dashboard'))

# Student registration
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
        try:
            conn.execute("INSERT INTO users (username,password,role,name,email) VALUES (?,?,?,?,?)",
                         (username, generate_password_hash(password), 'student', name, email))
            conn.commit()
            flash('Account created! Please login.', 'success')
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
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

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5050)
