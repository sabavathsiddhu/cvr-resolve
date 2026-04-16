# Fix: Store Data in Supabase (Connection Timeout Solution)

## Problem
Connection to `db.auneeeflawwqivzvdynw.supabase.co:5432` times out. This means port 5432 is blocked by your firewall or ISP.

## Solution: Use Supabase Connection Pooler

The connection pooler uses **port 6543** which is often not blocked.

### Step 1: Get Your Connection Pooler URL

1. Go to **https://supabase.com**
2. Login to your project
3. Click **Project Settings** (bottom left)
4. Go to **Database** tab
5. Look for **Connection pooler** section
6. Copy the connection string that looks like:
   ```
   postgresql://postgres.auneeeflawwqivzvdynw:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
   ```

### Step 2: Update .env File

Replace your current DATABASE_URL with the pooler URL:

```env
DATABASE_URL=postgresql://postgres.auneeeflawwqivzvdynw:Siddhu%402430@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
SUPABASE_URL=https://auneeeflawwqivzvdynw.supabase.co
SUPABASE_KEY=sb_publishable_naFmN8sh15fbku1R4dhW-g_voZmtflB
FLASK_SECRET_KEY=cvr_resolve_production_secret_2024_supabase_key
```

### Step 3: Restart the App

```bash
# From cvr_resolve folder:
python -m flask run --host=0.0.0.0 --port=5000
```

---

## Alternative Solutions (if pooler doesn't work)

### Option 1: Check Your Firewall
- Windows Firewall might be blocking port 5432
- Go to **Windows Defender → Firewall & Network** → Check **Allow an app through firewall**
- If needed, add Python to allowed apps

### Option 2: Use SSH Tunnel (Advanced)
```bash
# Create SSH tunnel to Supabase (if they provide SSH access)
ssh -L 5432:db.auneeeflawwqivzvdynw.supabase.co:5432 user@jump-host
```

### Option 3: Contact Your ISP/Network Admin
- Some ISPs block port 5432 for security
- Ask them to whitelist Supabase's IP addresses

### Option 4: Use VPN
- Connect to a VPN service
- Then try connecting to Supabase (port might not be blocked there)

---

## Verify Connection Works

Run this test:

```bash
python test_supabase.py
```

If it shows "✅ Connected!", you're good to go.

If still times out, try the pooler connection (port 6543).

---

## Once Connected: Migrate Data

If you've been using SQLite (app_sqlite.py), data is stored locally. To migrate to Supabase:

1. Run the init script:
   ```bash
   python init_database.py
   ```

2. Manually add users to Supabase via:
   - Supabase Dashboard → SQL Editor
   - Or use the app's registration form

3. Switch back to `app.py`:
   ```bash
   python -m flask run
   ```

Now all new data will be stored in Supabase!
