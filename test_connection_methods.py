import os
import psycopg2
from dotenv import load_dotenv
import sys

load_dotenv('cvr_resolve/.env')

print("=" * 60)
print("Testing Supabase Connection Methods")
print("=" * 60)

# Method 1: Try Connection Pooler (Port 6543)
print("\n[1] Testing Connection Pooler (Port 6543)...")
pooler_url = os.getenv('DATABASE_URL_POOLER')
if pooler_url:
    try:
        conn = psycopg2.connect(pooler_url, connect_timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        print("✅ Connection Pooler: SUCCESS")
        print(f"   Use this in .env: {pooler_url[:80]}...")
    except Exception as e:
        print(f"❌ Connection Pooler failed: {str(e)[:100]}")
else:
    print("⚠️  DATABASE_URL_POOLER not set")

# Method 2: Try Direct Connection (Port 5432)
print("\n[2] Testing Direct Connection (Port 5432)...")
db_url = os.getenv('DATABASE_URL')
if db_url:
    try:
        conn = psycopg2.connect(db_url, connect_timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        print("✅ Direct Connection: SUCCESS")
    except psycopg2.OperationalError as e:
        print(f"❌ Direct Connection failed: {str(e)[:100]}")

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
print("1. Go to: https://supabase.com → Your Project → Settings → Database")
print("2. Copy the Connection pooler URL (port 6543)")
print("3. Update .env with DATABASE_URL_POOLER=<pooler_url>")
print("4. Then run: python -m flask run (from cvr_resolve folder)")
print("=" * 60)
