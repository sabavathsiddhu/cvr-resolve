# PythonAnywhere Deployment Checklist

## Pre-Deployment (Do on your computer NOW)

- [ ] Change `app.py` last line: `app.run(debug=False, port=5050)`
- [ ] Verify `requirements.txt` contains all dependencies (NO gunicorn needed)
- [ ] Test app locally: `.\.venv\Scripts\python cvr_resolve\app.py`
- [ ] Confirm login works with demo credentials
- [ ] Create `.env.production` with:
  ```
  FLASK_SECRET_KEY=generate_random_32_char_string_here
  GOOGLE_CLIENT_ID=your_id_if_using_oauth
  GOOGLE_CLIENT_SECRET=your_secret_if_using_oauth
  ```

## Files to Upload

Upload these from `C:\Users\sabav\Downloads\cvr_resolve\cvr_resolve\` to `/home/yourusername/cvr-resolve/`:

```
✓ app.py
✓ config.py  
✓ requirements.txt
✓ templates/ (entire folder with 9 HTML files)
✓ static/ (entire folder with css/ js/ folders)
✓ instance/ (if exists, or create empty folder)
```

## PythonAnywhere Account Setup (5 minutes)

- [ ] Go to https://www.pythonanywhere.com
- [ ] Click "Sign Up" → Free Account
- [ ] Create username (this becomes your app URL)
- [ ] Verify email and login
- [ ] Note your username (you'll need it for paths)

## Upload Files (5 minutes)

**Option 1: Web Upload (Easier)**
- [ ] Click **Files** menu
- [ ] Navigate to `/home/yourusername/cvr-resolve/`
- [ ] Upload each file/folder listed above

**Option 2: Git Upload**
- [ ] Open **Bash console**
- [ ] Run: `git clone YOUR_REPO_URL cvr-resolve`

## Create Web App (2 minutes)

- [ ] Click **Web** tab
- [ ] Click **Add a new web app**
- [ ] Choose **Manual configuration**
- [ ] Select **Python 3.11**
- [ ] Click **Next**

## Install Dependencies (3 minutes)

- [ ] Go to **Bash console**
- [ ] Run these commands:
  ```bash
  cd /home/yourusername/cvr-resolve
  python3.11 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

## Configure WSGI (3 minutes)

- [ ] In **Web** tab, click WSGI config file path
- [ ] Copy the template code from `PYTHONANYWHERE_DEPLOYMENT.md` (Step 5)
- [ ] Replace `yourusername` with YOUR actual username
- [ ] Replace secret key with random 32 characters
- [ ] Add Google OAuth credentials if using them
- [ ] Click **Save**

## Configure Static Files (2 minutes)

In **Web** tab, **Static files** section, add:

| URL | Directory |
|-----|-----------|
| `/static` | `/home/yourusername/cvr-resolve/static` |
| `/uploads` | `/home/yourusername/cvr-resolve/static/uploads` |

## Deploy! (1 minute)

- [ ] Click **Reload** button (large green button on Web tab)
- [ ] Wait 10 seconds
- [ ] Visit: `https://yourusername.pythonanywhere.com`

## Test Live App (5 minutes)

- [ ] App loads without errors
- [ ] Login with `student1` / `stud123`
- [ ] Submit a test complaint
- [ ] View complaint in dashboard
- [ ] Logout
- [ ] Try registering new account
- [ ] Login as new user

## Troubleshooting Checklist

If app doesn't load:

- [ ] Check **Error log** in Web tab (click at bottom)
- [ ] Verify WSGI file has correct `yourusername` paths
- [ ] Confirm virtualenv path is correct
- [ ] Ensure all files uploaded to correct location
- [ ] Try **Reload** button again
- [ ] Wait 30 seconds, refresh browser with `Ctrl+F5`

If database error:
- [ ] Create `/home/yourusername/cvr-resolve/instance/` folder
- [ ] Run: `mkdir -p instance`
- [ ] Reload app

If static files missing:
- [ ] Verify `/static` and `/uploads` folders exist
- [ ] Check static files mapping is correct
- [ ] Create missing folders manually if needed

## Demo Credentials for Testing

| Role | Username | Password | What They Can Do |
|------|----------|----------|------------------|
| Student | `student1` | `stud123` | Submit complaints, view own complaints |
| Admin | `cm_admin` | `admin123` | Manage CM Block complaints |
| Super Admin | `superadmin` | `super123` | View all complaints, create admins |

## Success = You See This

✅ Login page loads  
✅ Can login with credentials  
✅ Dashboard shows complaints  
✅ Can submit new complaint  
✅ Can upload image with complaint  
✅ Admin can view complaints  
✅ Super Admin can see analytics  

## Estimated Total Time: 25-30 minutes

---

## Quick Command Reference

**Remove old venv and reinstall (if issues):**
```bash
rm -rf /home/yourusername/cvr-resolve/venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Restart app:**
```bash
# Go to Web tab, click Reload button
```

**View error log:**
```bash
# Go to Web tab, scroll to bottom, click Error log
```

**Access bash console:**
```bash
# Top menu: Bash console
```

---

**When you're done: Share your URL!**

Your live app will be at: `https://yourusername.pythonanywhere.com`

Email it to: teachers, classmates, college coordinators

**Always test locally first before uploading!**
