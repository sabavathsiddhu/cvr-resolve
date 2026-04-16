# Updated DATABASE_URL using Supabase Connection Pooler
# This uses port 6543 instead of 5432 - may bypass firewall blocks

DATABASE_URL=postgresql://postgres.auneeeflawwqivzvdynw:[password]@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
SUPABASE_URL=https://auneeeflawwqivzvdynw.supabase.co
SUPABASE_KEY=sb_publishable_naFmN8sh15fbku1R4dhW-g_voZmtflB  
FLASK_SECRET_KEY=cvr_resolve_production_secret_2024_supabase_key

# INSTRUCTIONS:
# 1. Replace [password] with your actual database password (Siddhu%402430)
# 2. Go to Supabase Dashboard → Project Settings → Database
# 3. Find Connection Pooler section and copy the connection string
# 4. Update DATABASE_URL above with that pooler connection string
# 5. The pooler URL format: postgresql://postgres:[PASSWORD]@[POOLER-HOST]:6543/postgres?sslmode=require
