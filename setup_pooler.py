#!/usr/bin/env python3
"""
Quick setup helper for Supabase Connection Pooler
"""
import os
from dotenv import load_dotenv

load_dotenv('cvr_resolve/.env')

print("\n" + "="*70)
print("🔧 Supabase Connection Pooler Setup Helper")
print("="*70 + "\n")

# Check current .env
db_url = os.getenv('DATABASE_URL')
db_pooler = os.getenv('DATABASE_URL_POOLER')

print("📊 Current Configuration:")
print(f"   Direct Connection (port 5432): {'✅ Set' if db_url else '❌ Missing'}")
print(f"   Connection Pooler (port 6543): {'✅ Set' if db_pooler else '❌ Missing'}")

if not db_pooler:
    print("\n⚠️  Connection Pooler NOT configured!")
    print("\n📝 Quick Setup Instructions:\n")
    print("1. Go to: https://supabase.com/dashboard")
    print("2. Select your project (auneeeflawwqivzvdynw)")
    print("3. Click Settings → Database → Connection pooler")
    print("4. Copy the connection string")
    print("5. Open cvr_resolve/.env")
    print("6. Add this line at the top (paste your pooler URL):")
    print("   DATABASE_URL_POOLER=postgresql://postgres.auneeeflawwqivzvdynw:Siddhu%402430@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require")
    print("\n   ⚠️  Make sure to:")
    print("      - Replace the region (aws-0-us-east-1) with YOUR region")
    print("      - Replace [PASSWORD] with: Siddhu%402430")
    print("      - Use URL encoding: %40 for @, %23 for #, etc.")
    print("\n7. Save the file")
    print("8. Run: cd cvr_resolve && python -m flask run")
else:
    print("\n✅ Connection Pooler is configured!")
    print(f"   URL: {db_pooler[:80]}...")

print("\n" + "="*70)
print("Next Steps:")
print("  1. Save your updated .env file")
print("  2. Run: python init_database.py")
print("  3. Run: cd cvr_resolve && python -m flask run --host=0.0.0.0 --port=5000")
print("  4. Test at: http://localhost:5000")
print("="*70 + "\n")
