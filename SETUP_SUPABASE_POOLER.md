# ✅ STEP-BY-STEP: Fix Supabase Data Storage

## The Problem
Connection to Supabase times out on port 5432 (likely blocked by firewall/ISP).

## The Solution  
Use Supabase **Connection Pooler** (port 6543) instead of direct connection (port 5432).

---

## 📋 STEPS TO FIX

### Step 1: Get Your Connection Pooler URL

1. **Go to Supabase Dashboard:**
   - Visit: https://supabase.com
   - Login to your account
   - Select your project: `auneeeflawwqivzvdynw`

2. **Find Connection Pooler:**
   - Click **Settings** (gear icon) → **Database** → **Connection pooler**
   - You'll see a URL like:
     ```
     postgresql://postgres.auneeeflawwqivzvdynw:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
     ```
   - ⚠️  **Replace [PASSWORD]** with your actual password: `Siddhu%402430`

3. **Copy the complete URL** (with password replaced)

---

### Step 2: Update Your .env File

Edit `cvr_resolve/.env` and add this line **at the top**:

```env
DATABASE_URL_POOLER=postgresql://postgres.auneeeflawwqivzvdynw:Siddhu%402430@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
DATABASE_URL=postgresql://postgres:Siddhu%402430@db.auneeeflawwqivzvdynw.supabase.co:5432/postgres
SUPABASE_URL=https://auneeeflawwqivzvdynw.supabase.co
SUPABASE_KEY=sb_publishable_naFmN8sh15fbku1R4dhW-g_voZmtflB
FLASK_SECRET_KEY=cvr_resolve_production_secret_2024_supabase_key
```

**IMPORTANT**: 
- Replace `aws-0-us-east-1` with the region shown in YOUR Supabase dashboard (might be `us-east-1` or different)
- Replace `[PASSWORD]` with `Siddhu%402430`

---

### Step 3: Initialize Supabase Database

Run this to create tables in Supabase:

```bash
cd c:\Users\sabav\Downloads\cvr_resolve
python init_database.py
```

---

### Step 4: Run the Flask App

```bash
cd cvr_resolve
python -m flask run --host=0.0.0.0 --port=5000
```

The app will now:
- ✅ Try Connection Pooler (port 6543) first
- ✅ Store all data in Supabase
- ✅ Fallback to direct connection if needed

---

### Step 5: Verify It Works

1. Open browser: http://localhost:5000
2. Try login with demo account:
   - Username: `superadmin`
   - Password: `super123`
3. Create a complaint and submit
4. Go to Supabase Dashboard → **SQL Editor**
5. Run: `SELECT COUNT(*) FROM complaints;`
   - Should show the complaint you just created!

---

## 🆘 If Still Having Issues

### Issue: Still getting timeout
**Solution:**
- Double-check the pooler URL has the correct password and region
- Try the **direct connection** (port 5432) - it might work now
- Contact Supabase support if pooler is also blocked

### Issue: "Database connection failed"
**Solution:**
- Verify DATABASE_URL_POOLER is in .env
- Check the URL format has NO spaces
- Ensure password is URL-encoded: `%40` for `@`

### Issue: Tables don't exist
**Solution:**
- Run: `python init_database.py`
- This creates all tables in Supabase

---

## 📞 Need Help?

**Test connection status:**
```bash
python test_connection_methods.py
```

This will show which connections work!
