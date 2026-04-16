# Quick Start: CVR-Resolve with Supabase

## 🚀 30-Second Quickstart

### 1. Create Supabase Project (2 minutes)
- Go to https://supabase.com
- Sign up (email or GitHub)
- Click "New Project"
- Enter: Name = `cvr-resolve`, Password = (save it!)
- Wait for creation (takes a few minutes)

### 2. Get Credentials (1 minute)
In your Supabase dashboard:
```
Settings → Database → Connection String
```
Copy the connection string, looks like:
```
postgresql://postgres:PASSWORD@db.xxxxx.supabase.co:5432/postgres
```

### 3. Create .env File (1 minute)
In folder `cvr_resolve/cvr_resolve/`, create `.env`:

```
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_KEY=YOUR_ANON_KEY_HERE
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_ID.supabase.co:5432/postgres
FLASK_SECRET_KEY=your-random-secret-key-32-chars-min
```

Replace values with your actual credentials.

### 4. Install Dependencies (2 minutes)

```bash
# Activate virtual environment
venv\Scripts\activate

# Install new packages
pip install -r cvr_resolve/requirements.txt
```

### 5. Replace app.py (1 minute)

```bash
# Backup old app
move cvr_resolve\app.py cvr_resolve\app_sqlite.py

# Use new Supabase version
move cvr_resolve\app_supabase.py cvr_resolve\app.py
```

### 6. Start App (30 seconds)

```bash
python cvr_resolve\app.py
```

Expected output:
```
[OK] Database tables created
[OK] Demo data seeded successfully
 * Running on http://127.0.0.1:5050
```

### 7. Visit & Test (30 seconds)

Open browser: **http://127.0.0.1:5050**

Login: `student1` / `stud123`

**Done! ✅**

---

## 📋 Getting Credentials - Detailed

### Find SUPABASE_URL
1. Dashboard → Settings (bottom left) → API
2. You'll see:
   ```
   Project URL: https://xxxxxxxx.supabase.co
   ```
3. Copy that URL

### Find DATABASE_URL
1. Settings → Database
2. Scroll to "Connection pooling" or "Connection string"
3. Copy the PostgreSQL connection string
4. It looks like:
   ```
   postgresql://postgres:YOUR_PASSWORD@db.xxxxxxxx.supabase.co:5432/postgres
   ```

### Find SUPABASE_KEY
1. Settings → API
2. Copy the "anon public" key

### Generate FLASK_SECRET_KEY
In terminal:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output (32 character hex string)

---

## ✅ Verify Connection

After starting app, check Supabase dashboard:

**SQL Editor:**
```sql
SELECT * FROM users;
SELECT * FROM complaints;
```

Should return:
- 6 users (demo data)
- 0 complaints (empty)

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### "DATABASE_URL not set"
- Create .env file in `cvr_resolve/cvr_resolve/`
- Add all variables from .env.supabase.example
- Restart app

### "connection refused" or "network error"
- Verify DATABASE_URL is correct
- Check Supabase project is active (not paused)
- Restart Flask app

### App crashes on startup
- Check .env file exists and FORMAT is correct
- No quotes needed around values
- Each line: `KEY=value` (no spaces around =)

---

## 🎓 Demo Credentials

| Role | User | Pass |
|------|------|------|
| Student | student1 | stud123 |
| Admin | cm_admin | admin123 |
| Super Admin | superadmin | super123 |

---

## 📱 Test Complete Workflow

1. **Login:** student1 / stud123
2. **Go to:** "Raise New Complaint"
3. **Fill:**
   - Title: "Test"
   - Description: "Testing Supabase"
   - Location: "CM Block"
   - Photo: (optional, any image)
4. **Submit** → Check Supabase!

In Supabase SQL Editor:
```sql
SELECT * FROM complaints;
```

You should see your new complaint!

---

## 🔄 Switch Back to SQLite (if needed)

```bash
# Restore SQLite version
move cvr_resolve\app.py cvr_resolve\app_supabase.py
move cvr_resolve\app_sqlite.py cvr_resolve\app.py

# Restart
python cvr_resolve\app.py
```

---

## 📊 Supabase Features (Bonus!)

Now you have access to:

✅ **Real-time:** Change data and see updates instantly  
✅ **Backups:** Automatic daily backups  
✅ **REST API:** Built-in API for mobile apps  
✅ **Authentication (Optional):** Supabase Auth  
✅ **Storage:** File upload to Supabase  
✅ **Scalability:** Auto-scales as you grow  

---

## 🌐 Deploy to Production

With Supabase, you can deploy to:
- PythonAnywhere
- Heroku
- Railway
- Render
- Your own server

Database works everywhere because it's cloud-based!

---

**✅ You're ready! Start the app and enjoy Supabase! 🚀**
