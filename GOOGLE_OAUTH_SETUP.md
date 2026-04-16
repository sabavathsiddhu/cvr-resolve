# 🔐 Google OAuth Setup Guide for CVR Resolve

## Enable Google Login & Registration

This guide walks you through setting up Google OAuth2 authentication for CVR Resolve.

---

## Step 1: Get Google OAuth Credentials

### 1.1 Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a Project"** → **"New Project"**
3. Enter project name: `CVR Resolve` (or your choice)
4. Click **"Create"** and wait for project creation

### 1.2 Enable Google+ API
1. In Google Cloud Console, search for **"Google+ API"**
2. Click on **"Google+ API"** result
3. Click **"Enable"**

### 1.3 Create OAuth Consent Screen
1. In left sidebar, go to **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth 2.0 Client ID"**
3. If prompted, click **"Configure OAuth consent screen"** first
   - **User Type**: External (for testing)
   - **App name**: `CVR Resolve`
   - **User support email**: Your email
   - **Developer contact**: Your email
   - Click **"Save and Continue"**
4. Add scopes (click "Add or Remove Scopes"):
   - Search for and add:
     - `openid`
     - `email`
     - `profile`
   - Click **"Save and Continue"**
5. Add test users (your Gmail address)
6. Click **"Back to Dashboard"**

### 1.4 Create OAuth 2.0 Credentials
1. Go to **"Credentials"** in left sidebar
2. Click **"Create Credentials"** → **"OAuth 2.0 Client ID"**
3. **Application type**: Web application
4. **Name**: `CVR Resolve Web Client`
5. Under **"Authorized redirect URIs"**, add:
   ```
   http://localhost:5050/google_callback
   http://127.0.0.1:5050/google_callback
   https://yourdomain.com/google_callback (if deploying)
   ```
6. Click **"Create"**
7. Copy the **Client ID** and **Client Secret** (save these!)

---

## Step 2: Configure CVR Resolve

### 2.1 Create `.env` File

Create a file named `.env` in the `cvr_resolve/` directory:

```bash
# Windows - in cvr_resolve folder
echo. > .env
```

### 2.2 Add Credentials to `.env`

Open `.env` in a text editor and add:

```env
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET
FLASK_SECRET_KEY=cvr_resolve_secret_key_2024
ALLOWED_STUDENT_DOMAINS=@student.cvr.ac.in,@cvr.ac.in,gmail.com
```

**Where to get these values:**
- **GOOGLE_CLIENT_ID**: From Google Cloud Console credentials page
- **GOOGLE_CLIENT_SECRET**: From Google Cloud Console credentials page
- Keep other values as-is

### 2.3 Example `.env` File

```env
# Google OAuth Credentials
GOOGLE_CLIENT_ID=123456789-abc123def456ghi789.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-1a2b3c4d5e6f7g8h9i0j

# Flask Configuration
FLASK_SECRET_KEY=cvr_resolve_secret_key_2024

# Allowed student email domains (comma-separated)
ALLOWED_STUDENT_DOMAINS=@student.cvr.ac.in,@cvr.ac.in,gmail.com
```

---

## Step 3: Install Dependencies

```bash
# Navigate to project root
cd c:\Users\sabav\Downloads\cvr_resolve

# Install new packages
pip install -r cvr_resolve/requirements.txt
```

**New packages installed:**
- `google-auth-oauthlib==1.2.0` - Google OAuth
- `google-auth==2.28.0` - Google authentication
- `requests==2.31.0` - HTTP requests
- `python-dotenv==1.0.0` - Environment config

---

## Step 4: Run the Application

```bash
cd cvr_resolve
python app.py
```

Then open: **http://127.0.0.1:5050**

---

## Step 5: Test Google Authentication

### Test Login with Google

1. Click **"Sign in with Google"** on login page
2. Use your test Gmail account (the one you added to Google Project)
3. Grant permissions when prompted
4. You'll be logged in as a student!

### Test Registration with Google

1. Click **"Create Student Account"** (new account)
2. Look for **"Sign up with Google"** button
3. Use a different test Gmail account
4. Fill in username to complete registration
5. Account is created automatically!

---

## Troubleshooting

### Error: "GOOGLE_CLIENT_ID was not found"

**Solution**: 
- Make sure `.env` file exists in `cvr_resolve/` folder
- Check spelling of `GOOGLE_CLIENT_ID`
- Restart Flask app: `python app.py`

### Error: "Redirect URI mismatch"

**Solution**: 
- Go to Google Cloud Console → **Credentials**
- Edit the OAuth 2.0 Client ID
- Make sure redirect URI matches exactly:
  - Local: `http://127.0.0.1:5050/google_callback`
  - Production: `https://yourdomain.com/google_callback`

### Error: "invalid_client"

**Solution**:
- Double-check `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`
- Make sure spaces/tabs are not around the values
- Both must be from the **same** OAuth credentials

### Google button not showing

**Solution**:
- Hard refresh browser: `Ctrl+F5`
- Clear cache: `Ctrl+Shift+Delete`
- Check browser console for errors: `F12`

### Can't login with personal Gmail

**Solution**:
- Your Gmail account must be added as a test user in Google Cloud Console
- Only test users can login to app in development mode
- In production, this can be changed

---

## Features Added

✅ Students can login with Gmail
✅ Students can register with Gmail
✅ Google profile name auto-filled
✅ Google email auto-verified
✅ Works with regular username/password too
✅ Fallback to traditional login method

---

## Security Notes

- `.env` file should **NEVER** be committed to version control
- Add `.env` to `.gitignore`:
  ```
  echo .env >> .gitignore
  ```
- Keep `GOOGLE_CLIENT_SECRET` confidential
- In production, set `FLASK_SECRET_KEY` to a strong random value

---

## Production Deployment

When deploying to production (Heroku, AWS, etc.):

1. **Get your production domain**
2. Add to Google OAuth redirect URIs:
   ```
   https://yourdomain.com/google_callback
   ```
3. Set environment variables on hosting platform:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `FLASK_SECRET_KEY` (strong random value)
4. Update in Google Cloud Console to allow all users (not just test users)

---

## Customization

### Restrict Student Email Domains

Edit `.env`:
```env
# Only allow college email domain
ALLOWED_STUDENT_DOMAINS=@student.cvr.ac.in,@cvr.ac.in
```

### Change OAuth Scopes

If you want different permission scopes, edit `app.py` in the `google_login()` function:
```python
scope=openid%20email%20profile  # Current scopes
```

### Customize Welcome Message

Edit `templates/google_register.html` to change welcome text.

---

## Testing Checklist

- [ ] Google button appears on login page
- [ ] Google button appears on register page
- [ ] Can login with test Gmail account
- [ ] Can register new student with Gmail
- [ ] Profile name auto-filled from Google
- [ ] Email shown as verified
- [ ] Traditional username/password login still works
- [ ] Can switch between Google and regular login

---

## Support

If you have issues:

1. Check `.env` file exists and has correct credentials
2. Verify OAuth credentials are from same Google project
3. Check Google Cloud Console for errors
4. Hard refresh browser to clear cache
5. Restart Flask application

---

## Next Steps

✅ Setup complete! Now you can use Google authentication.

1. Test with available test accounts
2. Add more test users in Google Cloud Console
3. When ready for production, remove test user restrictions
4. Deploy to production and update OAuth URIs

**Happy authenticating!** 🔐

