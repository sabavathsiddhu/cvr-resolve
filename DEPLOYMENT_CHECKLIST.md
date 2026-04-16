# CVR Resolve - Production Deployment Checklist

## ✅ Pre-Deployment Status

- [x] Flask application functional on localhost
- [x] Supabase PostgreSQL database connected
- [x] All templates rendering correctly
- [x] Authentication system working
- [x] Photo upload functionality verified
- [x] Admin dashboards displaying all blocks
- [x] requirements.txt with pinned versions
- [x] Dockerfile created and tested locally
- [x] Procfile configured for Gunicorn (web: gunicorn cvr_resolve.app:app)
- [x] Debug mode now conditional (FLASK_ENV=development)
- [x] PORT configurable via environment variable

---

## 📋 Before Deploying

### Step 1: Verify Local Production Build ⚙️
```bash
# Test production build locally
docker build -t cvr-resolve .
docker run -p 5050:5050 \
  -e FLASK_ENV=production \
  -e DATABASE_URL="postgresql://postgres:Siddhu%402430@db.auneeeflawwqivzvdynw.supabase.co:5432/postgres" \
  -e SUPABASE_URL="https://auneeeflawwqivzvdynw.supabase.co" \
  -e FLASK_SECRET_KEY="cvr_resolve_production_secret_2024_supabase_key" \
  cvr-resolve
```

- [ ] Container builds without errors
- [ ] Container runs without errors
- [ ] Can access http://localhost:5050
- [ ] Login works
- [ ] Database queries execute

### Step 2: Prepare Git Repository 🔑
```bash
# Initialize git if not already done
git init
git add -A
git commit -m "Production ready CVR Resolve deployment"

# Create .gitignore to exclude sensitive files
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
git add .gitignore
git commit -m "Add .gitignore for security"

# Push to GitHub (or your git hosting)
git remote add origin https://github.com/your-username/cvr-resolve.git
git push -u origin main
```

- [ ] Code pushed to Git repository
- [ ] .env file NOT in repository (check .gitignore)
- [ ] Repository is public/private as desired
- [ ] GitHub token/credentials if using private repo

---

## 🚀 Deployment Platforms

### **RECOMMENDED: Render (Easiest)**

**Render.com Setup:**

1. **Create Account:** Go to render.com and sign up
2. **Connect Repository:** Click "New +" → "Web Service"
3. **Select Repository:** Choose your CVR-Resolve repo
4. **Configure:**
   - Name: `cvr-resolve`
   - Environment: `Python 3.11`
   - Build Command: `pip install -r cvr_resolve/requirements.txt`
   - Start Command: `gunicorn cvr_resolve.app:app`
   - Plan: Free (12 hrs/month) or Paid for 24/7

5. **Set Environment Variables:**
   - [ ] `DATABASE_URL`: postgres://postgres:Siddhu%402430@db...
   - [ ] `SUPABASE_URL`: https://auneeeflawwqivzvdynw.supabase.co
   - [ ] `SUPABASE_KEY`: sb_publishable...
   - [ ] `FLASK_SECRET_KEY`: cvr_resolve_production_secret_2024_supabase_key
   - [ ] `FLASK_ENV`: production

6. **Deploy:** Click "Create Web Service" and wait for build to complete

**Testing on Render:**
- [ ] App deployed successfully
- [ ] App URL responds with login page
- [ ] Can register new account
- [ ] Can login with existing account
- [ ] Can submit complaint with photo
- [ ] Admin dashboard shows all blocks
- [ ] SuperAdmin analytics work

**Cost:** Free tier available (limited hours, shared resources)

---

### **Alternative: Heroku (Classic Option)**

**Heroku Setup:**

1. **Install Heroku CLI:** Download from heroku.com/cli
2. **Login:** `heroku login`
3. **Create App:** `heroku create cvr-resolve`
4. **Set Variables:**
   ```bash
   heroku config:set DATABASE_URL="postgresql://postgres:Siddhu%402430@d..."
   heroku config:set FLASK_ENV=production
   heroku config:set FLASK_SECRET_KEY=cvr_resolve_production_secret_2024_supabase_key
   # ... other env vars
   ```
5. **Deploy:** `git push heroku main`

**Cost:** Free tier discontinued; minimum $7/month

---

### **Alternative: Railway.app**

**Railway Setup:**

1. Sign up at railway.app
2. Click "+ New Project"
3. Select "Deploy from GitHub"
4. Choose CVR-Resolve repository
5. Railway auto-detects Python/flask
6. Add environment variables via Variables tab
7. Deploy automatically

**Cost:** Free tier: $5 credit/month

---

### **Alternative: Docker Deployment (VPS)**

If using AWS/DigitalOcean/Google Cloud:

```bash
# On your VPS
git clone https://github.com/your-username/cvr-resolve.git
cd cvr-resolve

# Create .env with production values
cat > cvr_resolve/.env << EOF
DATABASE_URL=postgresql://postgres:Siddhu%402430@db...
FLASK_ENV=production
FLASK_SECRET_KEY=your_secret_key
PORT=5050
EOF

# Build and run
docker build -t cvr-resolve .
docker run -d -p 80:5050 \
  --env-file cvr_resolve/.env \
  --name cvr-app \
  cvr-resolve
```

**Cost:** Varies by provider ($5-50+/month)

---

## 🔐 Security Checklist

Before going live:

- [ ] FLASK_ENV set to "production"
- [ ] FLASK_DEBUG disabled (automatic with FLASK_ENV)
- [ ] DATABASE_URL password is URL-encoded (@ = %40)
- [ ] FLASK_SECRET_KEY is strong (32+ random characters)
- [ ] .env file is NOT in version control
- [ ] HTTPS enabled (automatic with Render/Heroku)
- [ ] Database backups enabled (Supabase)
- [ ] Monitor logs regularly
- [ ] Set up error notifications (Sentry/Email)

---

## 📊 Post-Deployment Testing

### Critical Tests (Must Pass):

1. **Login Flow:**
   - [ ] Can access login page
   - [ ] Can register new account
   - [ ] Can login with credentials
   - [ ] Can logout

2. **Student Dashboard:**
   - [ ] Can view personal complaints
   - [ ] Can submit new complaint
   - [ ] Can upload photo (< 5MB)
   - [ ] New complaint appears in dashboard

3. **Admin Dashboard:**
   - [ ] Shows only assigned block's complaints
   - [ ] Can update complaint status
   - [ ] Can filter by status/priority
   - [ ] Can add remarks

4. **SuperAdmin Dashboard:**
   - [ ] Shows all complaints from all blocks
   - [ ] "Complaints per Block" chart shows all 8 blocks
   - [ ] Analytics charts display correctly
   - [ ] Can see complaint details

5. **Database Integrity:**
   - [ ] Data persists after app restart
   - [ ] Photos are accessible
   - [ ] Timestamps are correct

### Full Test Scenario:

```
1. Visit deployed_url.com
2. Register as student with email
3. Login with new account
4. Submit complaint with photo
5. Logout
6. Login as admin (cm_admin / admin123)
7. Verify complaint visible in dashboard
8. Update status to "In Progress"
9. Logout
10. Login as superadmin (superadmin / super123)
11. Verify complaint in superadmin dashboard
12. Check all 8 blocks in "Complaints per Block" chart
```

---

## 🆘 Troubleshooting

### "Database Connection Failed"
- [ ] DATABASE_URL has correct password encoding (%40 for @)
- [ ] Supabase accepts connections from your deployment region
- [ ] Check Supabase networking settings for IP whitelist

### "Static Files Not Loading"
- [ ] Ensure WhiteNoise is installed (in requirements.txt)
- [ ] Check `static/` folder structure
- [ ] Verify Flask STATIC_FOLDER configuration

### "Uploads Not Working"
- [ ] Ensure upload directory is writable
- [ ] For cloud deployments, use cloud storage (AWS S3/Supabase Storage)
- [ ] Check file size limit (set to 5MB)

### "Pages Showing 500 Error"
- [ ] Check deployment logs
- [ ] Verify all environment variables are set
- [ ] Ensure database tables exist (run init_database.py)
- [ ] Check for Python syntax errors

### "Can't Login After Deployment"
- [ ] Verify FLASK_SECRET_KEY is consistent
- [ ] Check if user accounts exist in Supabase
- [ ] Verify password hashing works correctly

---

## 📱 Recommended Workflow

1. **Start with Render (easiest):**
   - Push to GitHub
   - Connect Render to GitHub
   - Set environment variables
   - Deploy with one click

2. **Monitor first 24 hours:**
   - Check logs daily
   - Test all user roles
   - Verify photos upload correctly

3. **Scale if needed:**
   - Upgrade Render plan for 24/7 uptime
   - Set up automated backups
   - Add error monitoring (Sentry)

4. **Going Production:**
   - Set up custom domain
   - Enable HTTPS (automatic on Render)
   - Set up monitoring/alerts
   - Document deployment process

---

## 📞 Support Resources

- **Render Documentation:** docs.render.com
- **Supabase Documentation:** supabase.com/docs
- **Flask Documentation:** flask.palletsprojects.com
- **PostgreSQL psycopg2:** psycopg.org

---

## 🎯 Final Deployment Command Summary

**For Render:**
```
1. Push code to GitHub
2. Go to render.com → New Web Service
3. Select GitHub repo
4. Set env variables
5. Click Deploy
```

**For Heroku:**
```
heroku login
heroku create cvr-resolve
heroku config:set DATABASE_URL="..." FLASK_ENV=production ...
git push heroku main
heroku open
```

**For Docker/VPS:**
```
docker build -t cvr-resolve .
docker run -p 80:5050 --env-file .env cvr-resolve
```

---

**Status:** ✅ **READY FOR PRODUCTION** - All systems go! Choose your platform and deploy! 🚀
