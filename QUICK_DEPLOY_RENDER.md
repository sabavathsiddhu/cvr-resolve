   # CVR Resolve - Quick Deployment to Render (5 Minutes)

## 🎯 Quickest Path to Production

**Total Time:** ~5 minutes (most time is waiting for Render to build)

---

## Step 1: Push Code to GitHub (2 minutes)

```bash
# Navigate to project directory
cd cvr_resolve

# Initialize git if not already done
git init
git add -A

# Create .gitignore for security
cat > .gitignore << EOF
.env
.env.local
.venv/
__pycache__/
*.pyc
instance/
dvr.db
.DS_Store
.idea/
EOF

git add .gitignore
git commit -m "CVR Resolve - production ready"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/cvr-resolve.git
git branch -M main
git push -u origin main
```

**Result:** ✅ Code is now on GitHub

---

## Step 2: Create Render Account (1 minute)

- Go to **render.com**
- Click "Sign Up"
- Use GitHub account to sign up (faster)
- Grant access to your GitHub account

**Result:** ✅ Render account created and connected to GitHub

---

## Step 3: Create New Web Service (1 minute)

1. Click **"New +"** in top right
2. Select **"Web Service"**
3. Select your **cvr-resolve** repository
4. Click **"Connect"**

**Web Service Settings:**
- **Name:** cvr-resolve  
- **Runtime:** Python 3
- **Build Command:** `pip install -r cvr_resolve/requirements.txt`
- **Start Command:** `gunicorn cvr_resolve.app:app`
- **Plan:** Free (select lower option for testing, or paid for 24/7)

Click **"Create Web Service"**

**Result:** ✅ Web service created, build starting

---

## Step 4: Add Environment Variables (1 minute)

While the app is building, add environment variables:

1. In your Render dashboard, go to **"Environment"** tab
2. Click **"Add Environment Variable"** and add these:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `DATABASE_URL` | `postgresql://postgres:Siddhu%402430@db.auneeeflawwqivzvdynw.supabase.co:5432/postgres` |
| `SUPABASE_URL` | `https://auneeeflawwqivzvdynw.supabase.co` |
| `SUPABASE_KEY` | `sb_publishable_naFmN8sh15fbku1R4dhW-g_voZmtflB` |
| `FLASK_SECRET_KEY` | `cvr_resolve_production_secret_2024_supabase_key` |
| `PORT` | `5050` |

3. Scroll down and click **"Save Changes"**

Render will automatically redeploy with the new variables.

**Result:** ✅ Environment variables set

---

## Step 5: Test Your Deployment (Verify)

When build completes (green checkmark appears):

1. Click the **URL** at the top of the page (e.g., `cvr-resolve.onrender.com`)
2. You should see **CVR Resolve Login** page

### Test Scenarios:

**Test 1 - Register as Student:**
- Click "Register"  
- Fill: Name, Email, Password, select "Student"
- Click "Register"
- Result: ✅ Account created, redirected to login

**Test 2 - Login:**
- Use credentials from Test 1
- Result: ✅ Logged in, see Student Dashboard

**Test 3 - Submit Complaint:**
- Click "Submit New Complaint"
- Fill all fields
- Upload a photo (PNG, JPG, GIF, WebP, max 5MB)
- Click "Submit"
- Result: ✅ Complaint appears in dashboard

**Test 4 - Login as Admin:**
- Logout (click "Logout" in top right)
- Login with: **cm_admin** / **admin123**
- Result: ✅ See Admin Dashboard with block-specific complaints

**Test 5 - Login as SuperAdmin:**
- Logout
- Login with: **superadmin** / **super123**
- Result: ✅ See all complaints + charts with all 8 blocks

---

## 🎉 You're Live!

Your app is now deployed at: **`https://cvr-resolve.onrender.com`** (or your custom URL)

---

## ⚙️ Optional: Enable 24/7 Uptime

By default, Render's free tier spins down after 15 minutes of inactivity.

**To keep it running 24/7:**
1. Go to **Settings** tab in Render
2. Subscription: Upgrade to **Paid** plan
3. Choose tier ($7/month recommended)
4. Click "Upgrade"

---

## 🌐 Optional: Add Custom Domain

1. Go to **Settings** → **Custom Domains**
2. Enter your domain (e.g., cvr-resolve.your-university.edu)
3. Add DNS records shown to your domain registrar
4. Click "Verify"

**Result:** Your app is at your custom domain!

---

## 📊 Monitor Your Deployment

**Render Dashboard shows:**
- ✅ Deployment status (green = live)
- 📊 CPU/Memory usage
- 📝 Live logs (click "Logs" tab)
- 🔄 Auto-redeploy on GitHub push

**To redeploy after code changes:**
```bash
git commit -am "Your changes"
git push origin main
# Render auto-deploys in 1-2 minutes
```

---

## 🆘 If Something Goes Wrong

**Check Logs:**
1. Click **"Logs"** tab in Render dashboard
2. Look for red errors
3. Common issues:
   - `DATABASE_URL not set` → Add to Environment variables
   - `psycopg2 not found` → requirements.txt missing psycopg2-binary
   - `ModuleNotFoundError` → Missing import, check requirements.txt

**Common Fixes:**
- **Restart service:** Click "Restart" button
- **Redeploy:** Click "Manual Deploy" → "Deploy latest commit"
- **Clear cache:** Click Settings → Scroll down → "Clear cache & redeploy"

---

## 💡 Pro Tips

1. **Faster builds:** Add `.dockerignore` to exclude large files
2. **Monitor errors:** Add Sentry integration (free tier available)
3. **Database backups:** Enable in Supabase console
4. **Custom domain:** Route through Cloudflare for better performance
5. **Check logs hourly first week** to catch issues early

---

## 📱 Share Your App

- **Deployed URL:** Share with friends/instructors
- **Demo Accounts:**
  - Student: student1 / stud123
  - Admin: cm_admin / admin123  
  - SuperAdmin: superadmin / super123

---

## ✅ Success Checklist

- [x] Code pushed to GitHub
- [x] Render account created
- [x] Web service created
- [x] Environment variables added
- [x] Build completed (green checkmark)
- [x] Login page loads
- [x] Can register/login
- [x] Can submit complaints
- [x] Admin dashboard works
- [x] SuperAdmin dashboard works

---

## 🚀 Next Steps

1. **Share the app** with your college
2. **Monitor logs** for first week
3. **Collect feedback** from users
4. **Scale infrastructure** if needed (Render paid plan)
5. **Add custom domain** for professional look

---

**Congratulations! 🎊 CVR Resolve is now live on the internet!**

For more deployment options, see `DEPLOYMENT_CHECKLIST.md`
