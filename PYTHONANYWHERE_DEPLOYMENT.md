# Deploy CVR-Resolve to PythonAnywhere (Complete Guide)

## Why PythonAnywhere?
✅ Free tier (no credit card needed)  
✅ Simple dashboard  
✅ Free SSL/HTTPS  
✅ Perfect for school projects  
✅ Permanent free URL  

---

## Step 1: Create PythonAnywhere Account

1. Go to **https://www.pythonanywhere.com**
2. Click **Sign Up** → Choose **Free Account**
3. Enter username (e.g., `cvrresolve`)
4. Verify email
5. Login to dashboard

**Your free URL will be:** `https://yourusername.pythonanywhere.com`

---

## Step 2: Upload Your Project Files

### Option A: Upload via Web Interface (Easier)

1. In PythonAnywhere dashboard, click **Files** (top menu)
2. Navigate or create folder: `/home/yourusername/cvr-resolve/`
3. Click **Upload a file** button
4. Upload these files/folders from `C:\Users\sabav\Downloads\cvr_resolve\cvr_resolve\`:
   - `app.py`
   - `config.py`
   - `requirements.txt`
   - `templates/` (entire folder)
   - `static/` (entire folder)
   - `instance/` (if it exists)

### Option B: Upload via Git (Advanced)

1. In PythonAnywhere **Bash console**, run:
```bash
cd /home/yourusername
git clone https://github.com/YOUR_REPO_URL cvr-resolve
cd cvr-resolve
```

---

## Step 3: Set Up Python Environment (Virtual Env)

1. Click **Bash console** (top menu)
2. Run these commands:

```bash
cd /home/yourusername/cvr-resolve
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-login werkzeug python-dotenv google-auth-oauthlib google-auth requests
```

**Expected output:** `Successfully installed...`

---

## Step 4: Create Web App

1. Go to **Web** tab (top menu)
2. Click **Add a new web app**
3. Choose **Manual configuration** (NOT Flask option)
4. Select **Python 3.11**
5. You'll see a configuration screen

---

## Step 5: Configure WSGI File

1. On the **Web** page, find **WSGI configuration file**
2. Click the file path (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Replace entire contents** with:

```python
# WSGI configuration for CVR-Resolve
import sys
import os

# Add your project directory to the path
path = '/home/yourusername/cvr-resolve'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_SECRET_KEY'] = 'your-secure-random-key-here-min-32-chars'
os.environ['GOOGLE_CLIENT_ID'] = 'your-google-client-id'  # Optional - for Google OAuth
os.environ['GOOGLE_CLIENT_SECRET'] = 'your-google-client-secret'  # Optional

# Import and configure Flask app
os.chdir(path)
from app import app
application = app

# Ensure database is initialized
from app import init_db
init_db()
```

4. Click **Save**

---

## Step 6: Update Requirements & Install

1. On **Web** page, find **Virtualenv** section
2. Should show: `/home/yourusername/.virtualenvs/cvr-resolve/` (or similar)
3. Click the path to open **Bash console** in that directory
4. Run:

```bash
pip install -r /home/yourusername/cvr-resolve/requirements.txt
```

**Include gunicorn? No** - PythonAnywhere handles WSGI directly

---

## Step 7: Configure Static & Media Files

1. On **Web** page, scroll to **Static files** section
2. Add these mappings:

| URL | Directory |
|-----|-----------|
| `/static` | `/home/yourusername/cvr-resolve/static` |
| `/uploads` | `/home/yourusername/cvr-resolve/static/uploads` |

**To add:**
- Click **Enter URL path**
- Enter `/static`
- Enter directory path
- Click reload button next to it

---

## Step 8: Modify app.py for PythonAnywhere

In your `app.py`, change the last 2 lines from:

```python
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5050)
```

To:

```python
if __name__ == '__main__':
    init_db()
    # For PythonAnywhere: run with debug=False
    app.run(debug=False, port=5050)
```

1. Go to **Files** → Navigate to `/home/yourusername/cvr-resolve/`
2. Click `app.py` to edit
3. Scroll to bottom
4. Change `debug=True` to `debug=False`
5. Click **Save**

---

## Step 9: Set Environment Variables (Optional - For Google OAuth)

If you want Google login to work:

1. From your Google Cloud Console, get:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`

2. Edit the WSGI file (step 5) with actual values:
```python
os.environ['GOOGLE_CLIENT_ID'] = 'your-actual-client-id-from-google'
os.environ['GOOGLE_CLIENT_SECRET'] = 'your-actual-client-secret'
```

3. Click **Save**

---

## Step 10: Reload & Test

1. On **Web** page, click the big green **Reload** button
2. Wait 10 seconds
3. Visit your app URL: `https://yourusername.pythonanywhere.com`

---

## Step 11: Login & Test Features

**Demo Credentials:**

| Role | Username | Password |
|------|----------|----------|
| Student | `student1` | `stud123` |
| Admin | `cm_admin` | `admin123` |
| Super Admin | `superadmin` | `super123` |

Or register a new account:
- Click **Register**
- Fill form
- Login with new credentials

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

**Solution:**
1. Go to **Bash console**
2. Run: `pip install flask flask-login werkzeug python-dotenv`
3. Reload web app

### "No such file or directory: cvr.db"

**Solution:**
- App auto-creates database on first run
- If error persists, create `/home/yourusername/cvr-resolve/instance/` folder manually

### "Error 500: Internal Server Error"

**Solution:**
1. Check **Error log** (on Web page)
2. Scroll to bottom for latest error
3. Common fixes:
   - Verify WSGI file is correct
   - Check virtualenv path
   - Reload web app
   - Restart bash console

### App loads but images don't show

**Solution:**
1. Verify static files mapping (Step 7)
2. Check `/uploads` folder exists:
```bash
ls -la /home/yourusername/cvr-resolve/static/uploads/
```
3. If missing, create it:
```bash
mkdir -p /home/yourusername/cvr-resolve/static/uploads
```

---

## Accessing Your Live App

**Public URL:** `https://yourusername.pythonanywhere.com`

**Share this link with:**
- Teachers for review
- Classmates for testing
- College administration

---

## Advanced: Enable HTTPS (Free SSL)

PythonAnywhere provides free HTTPS automatically!

1. Go to **Web** page
2. Find **Security** section
3. Toggle **Force HTTPS** ON
4. All traffic automatically redirects to HTTPS

---

## Daily Usage

### Check App Status
1. Dashboard → **Web**
2. Green circle = running
3. Red circle = error

### View Logs
1. **Web** page → **Error log** (bottom)
2. **Web** page → **Server log**

### Restart App
1. Click **Reload** button (green circle)
2. Wait 5 seconds

### Update Code
1. Edit files via **Files** dashboard
2. Click **Reload** to apply changes (no restart needed!)

---

## Next Steps

1. **Test all features** locally first
2. **Verify Google OAuth** credentials (if using)
3. **Create backups** of database
4. **Share URL** with users
5. **Monitor errors** regularly

---

## Database Backup

To backup complaints data:

1. Go to **Bash console**
2. Run:
```bash
cp /home/yourusername/cvr-resolve/instance/cvr.db ~/backup_cvr.db
```

3. Download from **Files** dashboard

---

## Still Having Issues?

1. Check error log (detailed error messages)
2. File permissions: `chmod -R 755 /home/yourusername/cvr-resolve/`
3. Clear app cache: Visit `https://yourusername.pythonanywhere.com/logout` then login
4. Force reload: `Ctrl+Shift+R` in browser

---

## Success Indicators

✅ App loads without errors  
✅ Login works with demo credentials  
✅ Can submit new complaint  
✅ Dashboard updates show complaints  
✅ Admin can view and update complaints  
✅ Images upload successfully  

If all working → **Deployment complete!** 🎉

---

## Support Contacts

**PythonAnywhere Help:**
- https://help.pythonanywhere.com
- Forums: https://www.pythonanywhere.com/forums/

**Need Flask help?**
- Discord: https://discord.gg/flask
- Stack Overflow: Tag `flask`

---

**Your app is now live! Share the link and start managing complaints.** 🚀
