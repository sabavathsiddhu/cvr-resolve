# CVR-Resolve Production Deployment Guide

## Quick Overview
Your Flask app is production-ready. Choose one deployment option below:

---

## Option 1: Deploy to Heroku (Easiest - FREE tier available)

### Step 1: Prepare Files
```bash
cd c:\Users\sabav\Downloads\cvr_resolve
```

### Step 2: Create Procfile
```
web: gunicorn app:app
```

### Step 3: Update requirements.txt
Add Gunicorn:
```
flask>=2.3.0
flask-login>=0.6.2
werkzeug>=2.3.0
python-dotenv>=1.0.0
google-auth-oauthlib>=1.2.0
google-auth>=2.28.0
requests>=2.31.0
gunicorn>=21.0.0
```

### Step 4: Set Production Config
In `app.py`, change the last line to:
```python
if __name__ == '__main__':
    init_db()
    app.run(debug=False, port=5050)  # Change debug=True to debug=False
```

### Step 5: Deploy
```bash
# Install Heroku CLI, then:
heroku login
heroku create your-app-name
git push heroku main
```

**Result:** Your app runs at `https://your-app-name.herokuapp.com`

---

## Option 2: Deploy to PythonAnywhere (FREE tier available)

### Step 1: Sign Up
Go to https://www.pythonanywhere.com (free account)

### Step 2: Upload Files
- Upload `cvr_resolve/` folder
- Upload `requirements.txt`

### Step 3: Configure WSGI
In PythonAnywhere dashboard:
- Create new web app
- Point to your `app.py`
- Add Python 3.11 venv
- Run: `pip install -r requirements.txt`

### Step 4: Configure .env
Set environment variables in PythonAnywhere:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `FLASK_SECRET_KEY`

**Result:** Your app runs at `https://yourusername.pythonanywhere.com`

---

## Option 3: Deploy to AWS (with free tier for 12 months)

### Using Elastic Beanstalk
```bash
# Install AWS CLI
pip install awsebcli-ce

# Initialize
eb init

# Create environment
eb create cvr-resolve-env

# Deploy
eb deploy

# View live
eb open
```

**Result:** Your app runs on AWS with auto-scaling

---

## Option 4: Deploy to DigitalOcean (Simple & Affordable)

### Step 1: Create Droplet
- Choose Ubuntu 22.04 LTS
- Size: $6/month minimum

### Step 2: SSH into server
```bash
ssh root@your_server_ip
```

### Step 3: Install dependencies
```bash
apt update && apt install -y python3-pip python3-venv nginx supervisor
```

### Step 4: Clone/Upload app
```bash
git clone your-repo-url /var/www/cvr-resolve
cd /var/www/cvr-resolve
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Configure Gunicorn
Create `/etc/supervisor/conf.d/cvr-resolve.conf`:
```ini
[program:cvr-resolve]
directory=/var/www/cvr-resolve/cvr_resolve
command=/var/www/cvr-resolve/venv/bin/gunicorn app:app
autostart=true
autorestart=true
user=www-data
```

### Step 6: Configure Nginx
Point to localhost:8000 where Gunicorn runs

**Result:** Your app runs at `https://your-domain.com`

---

## Option 5: Docker + Cloud Run (Google Cloud)

### Create Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_SECRET_KEY=your-secret
ENV GOOGLE_CLIENT_ID=your-client-id
ENV GOOGLE_CLIENT_SECRET=your-secret
EXPOSE 5050
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "app:app"]
```

### Deploy to Cloud Run
```bash
gcloud run deploy cvr-resolve --source . --platform managed --region us-central1
```

**Result:** Scalable, serverless deployment with auto-HTTPS

---

## Recommended Path for Your Use Case

**Best for School Demo:** Option 2 (PythonAnywhere)
- Free tier, no credit card
- Simple setup
- Permanent URL
- Perfect for college project

**Best for Production:** Option 5 (Docker + Cloud Run)
- Auto-scaling
- Pay only for usage
- Professional infrastructure
- Easy to maintain

**Best for Learning:** Option 3 (AWS)
- Free tier for 12 months
- Industry-standard
- Great learning experience

---

## Pre-Deployment Checklist

- [ ] Change `debug=False` in app.py
- [ ] Set secure `FLASK_SECRET_KEY` (random 32 characters)
- [ ] Add `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to environment
- [ ] Test locally: `.\.venv\Scripts\python cvr_resolve\app.py`
- [ ] Update `requirements.txt` with gunicorn
- [ ] Create `.env.production` with production secrets
- [ ] Test with production settings locally
- [ ] Set up database backup plan (SQLite → PostgreSQL for production)

---

## Production Security Tips

1. **Use PostgreSQL instead of SQLite**
   - SQLite not recommended for concurrent access
   - Switch to: `pip install psycopg2-binary`

2. **Enable HTTPS/SSL**
   - Heroku: Automatic
   - PythonAnywhere: Included free
   - DigitalOcean: Use Let's Encrypt (Nginx)

3. **Secure Environment Variables**
   - Never commit `.env` to git
   - Use platform's secrets manager

4. **Database Backups**
   - Automated backups for SQLite
   - Daily exports recommended

5. **Monitoring**
   - Health checks on endpoints
   - Error logging (Sentry.io)
   - Performance monitoring

---

## Which Option Do You Want?

Reply with:
1. **PythonAnywhere** - Simplest, free
2. **Heroku** - Industry standard, easy
3. **DigitalOcean** - Affordable, full control
4. **AWS** - Powerful, free tier
5. **Docker + Cloud Run** - Scalable, serverless

I'll provide step-by-step deployment instructions for your choice!
