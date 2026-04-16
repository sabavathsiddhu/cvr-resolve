import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

print(f"Testing Web API for: {url}")

try:
    supabase: Client = create_client(url, key)
    # Just a simple check to see if we can reach the users table
    response = supabase.table("users").select("id").limit(1).execute()
    print("SUCCESS: Web API Connection Successful!")
except Exception as e:
    print(f"ERROR: Web API Connection Failed: {str(e)}")
