#!/usr/bin/env python3
"""
Initialize Supabase database tables, resetting the @PASSWORD encoding from .env
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import sys
from werkzeug.security import generate_password_hash

# Change to correct directory to find .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cvr_resolve', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not found in .env")
    sys.exit(1)

print("Connecting to Supabase...")
print(f"   Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'unknown'}")

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Connected to Supabase!")
    
    with conn.cursor() as c:
        # Drop existing tables if they exist (careful!)
        print("Setting up database tables...")
        
        # Create users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255),
                role VARCHAR(50) NOT NULL,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE,
                assigned_blocks TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Users table created")
        
        # Create complaints table
        c.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id SERIAL PRIMARY KEY,
                student_id INTEGER NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                image_path VARCHAR(255),
                location VARCHAR(255) NOT NULL,
                status VARCHAR(50) DEFAULT 'Pending',
                priority VARCHAR(50) DEFAULT 'Medium',
                remarks TEXT,
                duplicate_of INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        print("Complaints table created")
        
        conn.commit()
        
        # Check if already seeded
        with conn.cursor() as c:
            c.execute("SELECT COUNT(*) FROM users")
            user_count = c.fetchone()[0]
        
        if user_count == 0:
            print("Seeding demo data...")
            
            with conn.cursor() as c:
                # Super admin
                c.execute(
                    "INSERT INTO users (username, password, role, name, email) VALUES (%s, %s, %s, %s, %s)",
                    ('superadmin', generate_password_hash('super123'), 'superadmin', 'Super Admin', 'superadmin@cvr.ac.in')
                )
                
                # Block admins  
                admins = [
                    ('cm_admin', 'admin123', 'admin', 'CM Block Admin', 'cm@cvr.ac.in', '["CM Block"]'),
                    ('main_admin', 'admin123', 'admin', 'Main Block Admin', 'main@cvr.ac.in', '["Main Block"]'),
                    ('fy_admin', 'admin123', 'admin', 'First Year Admin', 'fy@cvr.ac.in', '["First Year Block"]'),
                    ('lab_admin', 'admin123', 'admin', 'Labs Admin', 'lab@cvr.ac.in', '["Labs Block","Library Block"]'),
                ]
                
                for admin in admins:
                    c.execute(
                        "INSERT INTO users (username, password, role, name, email, assigned_blocks) VALUES (%s, %s, %s, %s, %s, %s)",
                        (admin[0], generate_password_hash(admin[1]), admin[2], admin[3], admin[4], admin[5])
                    )
                
                # Students
                students = [
                    ('student1', 'stud123', 'student', 'Rahul Sharma', 'rahul@student.cvr.ac.in'),
                    ('student2', 'stud123', 'student', 'Priya Reddy', 'priya@student.cvr.ac.in'),
                ]
                
                for student in students:
                    c.execute(
                        "INSERT INTO users (username, password, role, name, email) VALUES (%s, %s, %s, %s, %s)",
                        (student[0], generate_password_hash(student[1]), student[2], student[3], student[4])
                    )
                
                conn.commit()
                print("Demo users created (6 total)")
                
                # Add sample complaints
                c.execute("SELECT id FROM users WHERE username='student1'")
                student_id = c.fetchone()[0]
                
                sample_complaints = [
                    (student_id, 'Broken AC', 'The AC in room 204 is not working', None, 'CM Block', 'Pending', 'High'),
                    (student_id, 'Water Leakage', 'Water leaking from ceiling', None, 'Labs Block', 'Pending', 'High'),
                ]
                
                for comp in sample_complaints:
                    c.execute(
                        "INSERT INTO complaints (student_id, title, description, image_path, location, status, priority) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        comp
                    )
                
                conn.commit()
                print("Sample complaints created")
        else:
            print(f"Database already has {user_count} users (skipping seeding)")
        
        print("\n" + "="*50)
        print("DATABASE SETUP COMPLETE!")
        print("="*50)
        print("\nDemo Credentials:")
        print("  Student: student1 / stud123")
        print("  Admin:   cm_admin / admin123")
        print("  Super Admin: superadmin / super123")
        print("\nStart your app with: python app.py")
        
except Exception as e:
    print(f"ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Verify Supabase project is ACTIVE (not paused)")
    print("2. Check DATABASE_URL is correct in .env")
    print("3. Test with: python test_supabase.py")
    sys.exit(1)
finally:
    try:
        conn.close()
    except:
        pass
