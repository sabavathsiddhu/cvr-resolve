import psycopg2
from dotenv import load_dotenv
import os

# Load from the correct path
load_dotenv('cvr_resolve/.env')

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env file!")
    print(f"Checked path: cvr_resolve/.env")
    exit(1)

print(f"Testing Supabase connection...")
print(f"DATABASE_URL: {DATABASE_URL[:50]}...")

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Connection successful!")
    
    with conn.cursor() as c:
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        print(f"✅ Users table exists: {user_count} users found")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print(f"\nTroubleshooting steps:")
    print(f"1. Check if Supabase project is ACTIVE (not paused)")
    print(f"2. Verify DATABASE_URL is correct in .env file")
    print(f"3. Ensure password special characters are URL-encoded")
    print(f"4. Check your internet connection")
