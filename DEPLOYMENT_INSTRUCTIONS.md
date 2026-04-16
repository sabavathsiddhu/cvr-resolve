# CVR-Resolve Deployment Instructions

## Quick Deployment to PythonAnywhere (Recommended - FREE)

### Step 1: Create PythonAnywhere Account
1. Go to https://www.pythonanywhere.com
2. Click **Sign Up** → Choose **Free Account**
3. Create username (e.g., `cvrresolve`)
4. Verify email and login

Your app will be deployed at: `https://yourusername.pythonanywhere.com`

---

### Step 2: Upload Project Files

From PythonAnywhere dashboard:
1. Click **Files** in top menu
2. Create folder: `/home/yourusername/cvr-resolve/`
3. Upload these files to that folder:
   - `cvr_resolve/app.py`
   - `cvr_resolve/config.py`
   - `cvr_resolve/requirements.txt`
   - `cvr_resolve/templates/` (entire folder)
   - `cvr_resolve/static/` (entire folder)
   - `.env` file (with your credentials)

---

### Step 3: Set Up Virtual Environment

In PythonAnywhere **Bash console**:
```bash
cd /home/yourusername/cvr-resolve
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Step 4: Configure WSGI File

1. Click **Web** in top menu
2. Click **Add a new web app**
3. Choose **Python 3.11**
4. Select **Manual configuration**
5. Edit the WSGI file (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):

```python
import sys
import os

path = '/home/yourusername/cvr-resolve'
if path not in sys.path:
    sys.path.append(path)

os.environ['FLASK_APP'] = 'app'
os.environ['FLASK_ENV'] = 'production'

# Load .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))

from app import app as application
```

6. Save and reload the web app

---

### Step 5: Configure Static Files

In PythonAnywhere **Web** tab:
- Add URL: `/static/`
- Directory: `/home/yourusername/cvr-resolve/cvr_resolve/static`

---

### Step 6: Set Environment Variables (Optional via PythonAnywhere)

In **Web** tab → **Environment variables**:
- `DATABASE_URL`: Your Supabase connection string
- `GOOGLE_CLIENT_ID`: Your Google OAuth ID
- `GOOGLE_CLIENT_SECRET`: Your Google OAuth Secret
- `FLASK_SECRET_KEY`: Your secret key

---

## Deployment Complete!

Your app is now live at: **https://yourusername.pythonanywhere.com**

To restart the app anytime:
- Click **Web** tab → Click **Reload button**

---

## Alternative Deployments

### Option: Local Docker Deployment
If Docker is installed on your machine:
```bash
docker build -t cvr-resolve .
docker run -p 5000:5000 --env-file .env cvr-resolve
```
Access at: `http://localhost:5000`

### Option: Heroku Deployment
1. Add `Procfile` to root directory:
   ```
   web: gunicorn cvr_resolve.app:app
   ```

2. Update `requirements.txt` to include `gunicorn>=21.0.0`

3. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

3. Set environment variables:
   ```bash
   heroku config:set DATABASE_URL="your-url"
   heroku config:set GOOGLE_CLIENT_ID="your-id"
   ```

---

## Troubleshooting

**502 Bad Gateway Error:**
- Check PythonAnywhere error logs
- Verify `.env` file exists with correct credentials
- Restart web app

**Database Connection Failed:**
- Verify `DATABASE_URL` is correct in `.env`
- Check Supabase connection settings
- Ensure database is running

**Static files not loading:**
- Verify static directory path in WSGI configuration
- Check file permissions

**Import errors:**
- Run `pip install -r requirements.txt` in venv
- Check Python version (3.11 required)
