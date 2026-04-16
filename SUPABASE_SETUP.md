# CVR-Resolve: Supabase Database Integration Guide

Complete guide to migrate from SQLite to Supabase PostgreSQL database.

---

## 🎯 Why Supabase?

✅ Cloud-hosted PostgreSQL database  
✅ Real-time updates support  
✅ Automatic backups & scalability  
✅ REST API built-in  
✅ 500MB free tier sufficient for college campus  
✅ Professional production-ready database  

---

## Step 1: Create Supabase Account (2 minutes)

1. Go to **https://supabase.com**
2. Click **"Start your project for free"**
3. Sign up with Email or GitHub
4. Verify email
5. Create new organization (e.g., "CVR College")
6. Create new project:
   - **Name:** cvr-resolve
   - **Password:** Generate strong password (save it!)
   - **Region:** Choose closest to you (e.g., us-east-1)
   - **Plan:** Free tier
7. Wait 2-3 minutes for project creation
8. You'll see: **Project URL** and **API Keys**

---

## Step 2: Get Database Connection Credentials (1 minute)

1. In Supabase dashboard, go to **Settings** (bottom left)
2. Click **Database**
3. Find **Connection String** section
4. Copy the connection string (looks like):
   ```
   postgresql://postgres:YOUR_PASSWORD@db.xxxxxxxxxxxx.supabase.co:5432/postgres
   ```
5. Also note your **Database Password** (you set in Step 1)

---

## Step 3: Update Python Dependencies

In your terminal, install PostgreSQL driver:

```bash
# Activate virtual environment first
venv\Scripts\activate

# Install Supabase Python package
pip install supabase
pip install psycopg2-binary
pip install python-dotenv

# Update requirements.txt
pip freeze > cvr_resolve/requirements.txt
```

---

## Step 4: Create .env File

Create file: `cvr_resolve/cvr_resolve/.env`

```
# Supabase Configuration
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_KEY=YOUR_ANON_KEY
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_ID.supabase.co:5432/postgres

# Flask Settings
FLASK_SECRET_KEY=generate-random-32-chars-here
```

### How to Get These Values:

**SUPABASE_URL:**
1. In Supabase dashboard, top-left see: `https://xxxxxxxxxxxx.supabase.co`
2. Copy that URL

**SUPABASE_KEY:**
1. Go to **Settings** → **API**
2. Copy **anon public** key

**DATABASE_URL:**
1. Go to **Settings** → **Database**
2. Copy the connection string

---

## Step 5: Update app.py to Use Supabase

Replace the entire database connection section with Supabase code.

### Original SQLite Code (Remove):
```python
DB_PATH = os.path.join(app.root_path, 'instance', 'cvr.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
```

### New Supabase Code (Add):
```python
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

class CursorContext:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    def __enter__(self):
        return self.cursor
    
    def __exit__(self, *args):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.commit()
```

---

## Step 6: Update Database Initialization

Replace SQLite schema with PostgreSQL schema:

### Old SQLite Code (Remove):
```python
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (...)''')
```

### New Supabase Code (Add):
```python
def init_db():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    conn = get_db()
    if not conn:
        print("Failed to connect to database")
        return
    
    try:
        with conn.cursor() as c:
            # Create users table
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255),
                    role VARCHAR(50) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE,
                    assigned_blocks TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create complaints table
            c.execute('''
                CREATE TABLE IF NOT EXISTS complaints (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL,
                    image_path VARCHAR(255),
                    location VARCHAR(255) NOT NULL,
                    status VARCHAR(50) DEFAULT 'Pending',
                    priority VARCHAR(50) DEFAULT 'Medium',
                    remarks TEXT,
                    duplicate_of INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES users(id)
                )
            ''')
            
            conn.commit()
            print("Database tables created successfully")
            
            # Seed demo data
            c.execute("SELECT COUNT(*) FROM users")
            if c.fetchone()[0] == 0:
                # Insert super admin
                c.execute(
                    "INSERT INTO users (username, password, role, name, email) VALUES (%s, %s, %s, %s, %s)",
                    ('superadmin', generate_password_hash('super123'), 'superadmin', 'Super Admin', 'superadmin@cvr.ac.in')
                )
                
                # Insert other data...
                conn.commit()
                print("Demo data seeded")
    
    except Exception as e:
        print(f"Database initialization error: {e}")
        conn.rollback()
    finally:
        conn.close()
```

---

## Step 7: Update Query Methods

All database queries need to use `%s` placeholders instead of `?`

### Example Changes:

**Old SQLite:**
```python
u = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
```

**New PostgreSQL:**
```python
with CursorContext(conn) as c:
    c.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    u = c.fetchone()
```

---

## Step 8: Complete Updated app.py

Here's the complete updated section (replace in your app.py):

```python
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os, json
from datetime import datetime
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'cvr_resolve_secret_key_2024')

# Supabase Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set!")

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

BLOCKS = ['CM Block', 'Main Block', 'First Year Block', 'Library Block', 'Hostel Block', 'Labs Block', 'Sports Block', 'Canteen Block']

def get_db():
    """Get database connection from Supabase"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def dict_from_row(cursor):
    """Convert psycopg2 RealDictCursor row to dict"""
    if cursor.description is None:
        return None
    cols = [desc[0] for desc in cursor.description]
    return dict(zip(cols, cursor.fetchone())) if cursor.rowcount > 0 else None

def init_db():
    """Initialize Supabase database with tables and seed data"""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    conn = get_db()
    
    if not conn:
        print("[ERROR] Failed to connect to Supabase database")
        return
    
    try:
        with conn.cursor() as c:
            # Users table
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255),
                    role VARCHAR(50) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE,
                    assigned_blocks TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Complaints table
            c.execute('''
                CREATE TABLE IF NOT EXISTS complaints (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL,
                    image_path VARCHAR(255),
                    location VARCHAR(255) NOT NULL,
                    status VARCHAR(50) DEFAULT 'Pending',
                    priority VARCHAR(50) DEFAULT 'Medium',
                    remarks TEXT,
                    duplicate_of INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
            print("[OK] Tables created")
            
            # Check if data already seeded
            c.execute("SELECT COUNT(*) as cnt FROM users")
            count = c.fetchone()[0]
            
            if count == 0:
                print("[SEEDING] Adding demo data...")
                
                # Super admin
                c.execute(
                    "INSERT INTO users (username, password, role, name, email) VALUES (%s, %s, %s, %s, %s)",
                    ('superadmin', generate_password_hash('super123'), 'superadmin', 'Super Admin', 'superadmin@cvr.ac.in')
                )
                
                # Block admins
                admins = [
                    ('cm_admin', 'admin123', 'admin', 'CM Block Admin', 'cm@cvr.ac.in', '["CM Block"]'),
                    ('main_admin', 'admin123', 'admin', 'Main Block Admin', 'main@cvr.ac.in', '["Main Block"]'),
                    ('fy_admin', 'admin123', 'admin', 'First Year Admin', 'fy@cvr.ac.in', '["First Year Block"]'),
                    ('lab_admin', 'admin123', 'admin', 'Labs Admin', 'lab@cvr.ac.in', '["Labs Block","Library Block"]'),
                ]
                
                for admin in admins:
                    c.execute(
                        "INSERT INTO users (username, password, role, name, email, assigned_blocks) VALUES (%s, %s, %s, %s, %s, %s)",
                        (admin[0], generate_password_hash(admin[1]), admin[2], admin[3], admin[4], admin[5])
                    )
                
                # Students
                students = [
                    ('student1', 'stud123', 'student', 'Rahul Sharma', 'rahul@student.cvr.ac.in'),
                    ('student2', 'stud123', 'student', 'Priya Reddy', 'priya@student.cvr.ac.in'),
                ]
                
                for student in students:
                    c.execute(
                        "INSERT INTO users (username, password, role, name, email) VALUES (%s, %s, %s, %s, %s)",
                        (student[0], generate_password_hash(student[1]), student[2], student[3], student[4])
                    )
                
                conn.commit()
                print("[OK] Demo data seeded")
    
    except Exception as e:
        print(f"[ERROR] Database initialization: {e}")
        conn.rollback()
    
    finally:
        conn.close()

# User model unchanged
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
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT * FROM users WHERE id=%s", (user_id,))
            u = c.fetchone()
            if u:
                return User(u['id'], u['username'], u['role'], u['name'], u['email'] or '', u['assigned_blocks'] or '[]')
    finally:
        conn.close()
    
    return None

# Rest of routes remain the same, but update queries to use %s instead of ?
# Example:

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        conn = get_db()
        if not conn:
            flash('Database error. Try again later.', 'danger')
            return render_template('login.html')
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as c:
                c.execute("SELECT * FROM users WHERE username=%s", (username,))
                u = c.fetchone()
                
                if u and check_password_hash(u['password'], password):
                    user_obj = User(u['id'], u['username'], u['role'], u['name'], u['email'] or '', u['assigned_blocks'] or '[]')
                    login_user(user_obj)
                    return redirect(url_for('dashboard'))
                
                flash('Invalid credentials.', 'danger')
        finally:
            conn.close()
    
    return render_template('login.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5050)
```

---

## Step 9: Update requirements.txt

Create file: `cvr_resolve/requirements.txt`

```
flask>=2.3.0
flask-login>=0.6.2
werkzeug>=2.3.0
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
supabase>=2.0.0
```

---

## Step 10: Test Connection Locally

```bash
# Activate venv
venv\Scripts\activate

# Install updated requirements
pip install -r cvr_resolve/requirements.txt

# Run app
python cvr_resolve/app.py
```

**Expected Output:**
```
[OK] Tables created
[OK] Demo data seeded
 * Running on http://127.0.0.1:5050
```

---

## Step 11: Verify in Supabase Dashboard

1. Go to **Supabase Dashboard**
2. Click **SQL Editor**
3. Run this query:
   ```sql
   SELECT COUNT(*) FROM users;
   SELECT COUNT(*) FROM complaints;
   ```
4. Should show:
   - 6 users (1 super admin + 4 admins + 2 students)
   - 0 complaints (empty)

---

## Step 12: Test Complete Workflow

1. **Visit:** http://127.0.0.1:5050
2. **Login:** student1 / stud123
3. **Submit complaint with photo**
4. **Check Supabase:**
   ```sql
   SELECT * FROM complaints;
   SELECT image_path FROM complaints;
   ```
5. Photo should be in `static/uploads/`

---

## Important Query Changes

### Replace all `?` with `%s`

| SQLite | PostgreSQL |
|--------|-----------|
| `WHERE id=?` | `WHERE id=%s` |
| `INSERT ... VALUES (?,?,?)` | `INSERT ... VALUES (%s,%s,%s)` |
| `UPDATE ... SET x=?` | `UPDATE ... SET x=%s` |

### Replace cursor operations

**SQLite:**
```python
conn.execute("SELECT * FROM users WHERE id=?", (id,)).fetchone()
```

**PostgreSQL:**
```python
with conn.cursor(cursor_factory=RealDictCursor) as c:
    c.execute("SELECT * FROM users WHERE id=%s", (id,))
    u = c.fetchone()
```

---

## Troubleshooting

### "psycopg2 connection refused"
- Check DATABASE_URL in .env is correct
- Verify Supabase project is active
- Restart app

### "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### "Missing .env file"
```bash
# Create it in cvr_resolve/cvr_resolve/.env with your credentials
```

### "Tables already exist"
- App will skip creation
- No error, just works

### "Foreign key constraint failed"
- When deleting user with complaints
- Delete complaints first, then user
- Or use CASCADE (already set)

---

## Backup Your Data

From Supabase Dashboard:
1. Go **SQL Editor**
2. Run:
   ```sql
   SELECT * FROM complaints;
   ```
3. Export as CSV
4. Save locally

---

## Migration Complete! ✅

Your app now uses:
- ✅ Supabase PostgreSQL (cloud database)
- ✅ Professional production setup
- ✅ Automatic backups
- ✅ Scalable infrastructure
- ✅ 500MB free storage

**Next Step:** Deploy to PythonAnywhere with Supabase backend!
