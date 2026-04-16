# Google OAuth Configuration for CVR Resolve

import os
from dotenv import load_dotenv

load_dotenv()

# Google OAuth Credentials (Set these environment variables)
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET')

# OAuth settings
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Session configuration
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Allowed email domains for student registration (optional)
# Set empty list to allow any domain
ALLOWED_STUDENT_DOMAINS = [
    '@student.cvr.ac.in',
    '@cvr.ac.in',
    'gmail.com',  # Allow any Gmail for demo
]

def is_allowed_student_email(email):
    """Check if email is allowed for student registration"""
    if not ALLOWED_STUDENT_DOMAINS:
        return True
    
    for domain in ALLOWED_STUDENT_DOMAINS:
        if domain.startswith('@'):
            if email.endswith(domain):
                return True
        else:
            if email.endswith(f'@{domain}'):
                return True
    return False
