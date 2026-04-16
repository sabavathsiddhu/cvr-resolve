import psycopg2
import sys

def test_connection(user, password, host, port, dbname):
    print(f"\n--- Testing: {user} @ {host}:{port} ---")
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
            sslmode='require',
            connect_timeout=5
        )
        print("SUCCESS! Connected.")
        conn.close()
        return True
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return False

# Your credentials
project_id = "auneeeflawwqivzvdynw"
password = "Siddhu@2430"

# regions to try
regions = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2",
    "ap-south-1", "ap-southeast-1", "ap-southeast-2",
    "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3"
]

for region in regions:
    host = f"aws-0-{region}.pooler.supabase.com"
    user = f"postgres.{project_id}"
    if test_connection(user, password, host, "6543", "postgres"):
        print(f"\nFOUND WORKING REGION: {region}")
        print(f"Use this in Render: postgresql://{user}:{password}@{host}:6543/postgres?sslmode=require")
        break
else:
    print("\nNo pooler regions worked. Please check if your project is 'Paused' in Supabase.")
