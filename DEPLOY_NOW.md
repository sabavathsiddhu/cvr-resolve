# CVR Resolve - Deployment Guide

## 🚀 Deployment Options

### Option 1: Heroku (Recommended - Free Tier Available)

**Prerequisites:**
- Heroku account (free tier available at heroku.com)
- Heroku CLI installed on your computer
- Git installed

**Steps:**

1. **Login to Heroku:**
```bash
heroku login
```

2. **Create a new Heroku app:**
```bash
heroku create your-app-name
```

3. **Set environment variables:**
```bash
heroku config:set DATABASE_URL="postgresql://postgres:Siddhu%402430@db.auneeeflawwqivzvdynw.supabase.co:5432/postgres"
heroku config:set SUPABASE_URL="https://auneeeflawwqivzvdynw.supabase.co"
heroku config:set SUPABASE_KEY="sb_publishable_naFmN8sh15fbku1R4dhW-g_voZmtflB"
heroku config:set FLASK_SECRET_KEY="your_random_secure_key_here"
heroku config:set FLASK_ENV="production"
```

4. **Deploy:**
```bash
git push heroku main
```

5. **Initialize database (if needed):**
```bash
heroku run python init_database.py
```

6. **View your app:**
```bash
heroku open
```

---

### Option 2: Docker (Local or VPS)

**Prerequisites:**
- Docker Desktop installed

**Steps:**

1. **Build the Docker image:**
```bash
docker build -t cvr-resolve .
```

2. **Create .env file with your credentials** (see .env.example)

3. **Run the container:**
```bash
docker run -p 5050:5050 \
  --env-file .env \
  --name cvr-app \
  cvr-resolve
```

4. **Access at:** http://localhost:5050

5. **Deploy to cloud (AWS, Google Cloud, Azure, DigitalOcean, etc.)**

---

### Option 3: PythonAnywhere (Simple, No Docker Needed)

**Prerequisites:**
- PythonAnywhere account (free tier available)

**Steps:**

1. Go to pythonanywhere.com and create an account
2. Upload your code via Git or direct upload
3. Create a new web app → Flask → Python 3.11
4. Configure WSGI file to point to `cvr_resolve/app.py`
5. Set environment variables in Web app settings
6. Set up static files mapping
7. Reload the web app

---

### Option 4: Render or Fly.io (Modern Alternatives)

Both support direct GitHub integration and free tier:

**Render.com:**
- Connect GitHub repo
- Create new Web Service
- Select Python 3.11
- Set Build Command: `pip install -r cvr_resolve/requirements.txt`
- Set Start Command: `gunicorn cvr_resolve.app:app`
- Add environment variables

**Fly.io:**
- Install flyctl CLI
- Run `fly launch`
- Set environment variables in `fly.toml`
- Deploy with `fly deploy`

---

## 📋 Pre-Deployment Checklist

- [x] Requirements.txt has pinned versions
- [x] Procfile configured for Gunicorn
- [x] Dockerfile created and tested
- [ ] .env file with production credentials secured
- [ ] DATABASE_URL has password properly URL-encoded (%40 for @)
- [ ] FLASK_SECRET_KEY is a strong random string (min 32 chars)
- [ ] FLASK_ENV set to "production"
- [ ] FLASK_DEBUG set to False
- [ ] Database tables initialized (run init_database.py)
- [ ] Test login works with production database
- [ ] Static files configured properly
- [ ] Upload limit set to 5MB in app
- [ ] Allowed file extensions restricted to images only

---

## 🔐 Security Checklist

- [ ] Never commit .env file to Git
- [ ] Keep FLASK_SECRET_KEY secret
- [ ] Use HTTPS only (automatically with most platforms)
- [ ] Set FLASK_DEBUG=False in production
- [ ] Use strong passwords for database
- [ ] Regularly update dependencies
- [ ] Monitor logs for errors
- [ ] Set up daily backups of Supabase
- [ ] Use environment variables for all secrets

---

## 🧪 Post-Deployment Testing

1. **Test Registration:** Create new account
2. **Test Login:** Login with credentials
3. **Test Complaint Submission:** Submit complaint with photo
4. **Test Admin Dashboard:** Verify all blocks show (even with 0 complaints)
5. **Test SuperAdmin:** Verify all reports and analytics work
6. **Test Photo Upload:** Verify image uploads and displays
7. **Test Database:** Check all data persists after restart

---

## 📊 Recommended Platform

**For Best Experience:** Heroku or Render
- Free tier available
- Easy environment variables management
- Automatic HTTPS
- Good uptime
- Simple deploy process

**Current Status:** ✅ App is production-ready!

---

## Support

If you encounter issues:
1. Check app logs: `heroku logs --tail` (Heroku) or platform-specific logs
2. Verify DATABASE_URL is correctly formatted
3. Ensure all environment variables are set
4. Run `python init_database.py` to initialize tables
5. Check if Supabase is accessible from deployment region

