# ❓ CVR Resolve - FAQ & Troubleshooting Guide

## Frequently Asked Questions

### Getting Started

**Q: How do I run the application?**
A: 
```bash
cd cvr_resolve
python app.py
```
Then open http://127.0.0.1:5050 in your browser.

**Q: I don't have Python installed. What do I do?**
A: Download Python 3.8+ from https://www.python.org/ and reinstall. Make sure to check "Add Python to PATH" during installation.

**Q: The port 5050 is already in use. What should I do?**
A: Edit `cvr_resolve/app.py`, find the last line:
```python
app.run(debug=True, port=5050)
```
Change `5050` to another port like `5051` and save.

**Q: It says "No module named 'flask'". What's wrong?**
A: You need to install dependencies. Run:
```bash
pip install -r cvr_resolve/requirements.txt
```

**Q: Do I need to create the database?**
A: No! The database is automatically created the first time you run the app.

---

### Demo Credentials

**Q: What are the demo usernames and passwords?**
A:
```
Super Admin:    superadmin / super123
CM Block Admin: cm_admin / admin123
Main Admin:     main_admin / admin123
First Year:     fy_admin / admin123
Labs Admin:     lab_admin / admin123
Student 1:      student1 / stud123
Student 2:      student2 / stud123
```

**Q: Can I create my own student account?**
A: Yes! Click "Create Student Account" on the login page.

**Q: Can I create my own admin account?**
A: No, only Super Admin can create admin accounts. Login as `superadmin` and use the "Add Admin" feature on the dashboard.

**Q: Can I change a demo password?**
A: The backend uses hashed passwords, so you cannot change them easily without code modification. For testing, just use the default passwords.

---

### Features & Usage

**Q: How do I submit a complaint as a student?**
A:
1. Login with `student1` / `stud123`
2. Click "New Complaint" in the sidebar
3. Fill in Title, Description, and select Location
4. Optionally upload an image
5. Click "Submit Complaint"

**Q: How do I update a complaint as an admin?**
A:
1. Login with your admin account (e.g., `cm_admin` / `admin123`)
2. You'll see all complaints for your assigned block
3. Click "Update" on the complaint you want to modify
4. Change the status to "Completed" or keep as "Pending"
5. Add remarks if needed
6. Click "Save Changes"

**Q: What's the difference between Pending and Completed?**
A: 
- **Pending**: Complaint is new and needs attention
- **Completed**: Admin has resolved the complaint

**Q: What's a "duplicate complaint"?**
A: If you submit a complaint similar to an existing one in the same location, the system automatically detects it and warns you. This helps prevent redundant work for admins.

**Q: How are priorities assigned?**
A:
- **High**: Keywords like "broken", "urgent", "emergency", "damaged"
- **Medium**: Regular complaints (default)
- **Low**: Keywords like "minor", "small", "suggest"

**Q: Can I upload an image with my complaint?**
A: Yes! The system supports PNG, JPG, GIF, and WEBP files up to 5MB.

**Q: Why can't I see complaints from other blocks as an admin?**
A: Block admins can only manage complaints from their assigned blocks. This is for security and organization.

**Q: How do I see all complaints as Super Admin?**
A:
1. Login as `superadmin` / `super123`
2. You'll see the main dashboard
3. All complaints from all blocks are displayed
4. Use filters to narrow down results

**Q: What do the charts on the Super Admin dashboard show?**
A:
- **Bar Chart**: Number of complaints per block
- **Doughnut Chart 1**: Pending vs Completed status ratio
- **Doughnut Chart 2**: Priority distribution (High/Medium/Low)

---

### Technical Issues

**Q: I get "ModuleNotFoundError: No module named 'flask'"**
A: You haven't installed dependencies. Run:
```bash
pip install -r cvr_resolve/requirements.txt
```

**Q: The app starts but shows "Failed to load /static/css/style.css"**
A: Make sure you're running the app from inside the `cvr_resolve` folder:
```bash
cd cvr_resolve
python app.py
```

**Q: I see "Error: address already in use"**
A: Another process is using port 5050. Either:
1. Kill the other process
2. Use a different port (see port change instructions above)

**Q: The database looks empty or wrong**
A: Delete `instance/cvr.db` and restart the app:
```bash
rm instance/cvr.db
python app.py
```

**Q: Images uploaded aren't showing**
A: Make sure the `static/uploads/` folder exists:
```bash
mkdir static/uploads
```
Restart the app.

**Q: I'm getting "Permission denied" errors**
A: On macOS/Linux, you might need to set permissions:
```bash
chmod 777 static/uploads
chmod 777 instance
```

**Q: The app crashes with "OperationalError: database is locked"**
A: The database is in use by another process. Restart Flask or delete the database file and recreate it.

---

### UI/UX Issues

**Q: The sidebar isn't showing on mobile**
A: Click the hamburger menu (☰) in the top-left corner to toggle the sidebar.

**Q: The dark theme is too dark for me**
A: You can modify colors in `static/css/style.css`. Look for the `:root` section at the top.

**Q: How do I change the background color?**
A: Edit `static/css/style.css` and find:
```css
:root {
  --bg: #0a0c10;
  --bg2: #111318;
  ...
}
```

**Q: Can I use light theme instead?**
A: The app is designed for dark theme. To create light theme, you'd need to modify all the CSS color variables, which is beyond the scope of this FAQ.

**Q: The layout looks broken on my phone**
A: Try:
1. Clear browser cache: Ctrl+Shift+Delete (Chrome)
2. Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
3. Try a different browser

**Q: Text is too small/too big**
A: Use browser zoom controls:
- **Zoom in**: Ctrl++ (Windows) or Cmd++ (Mac)
- **Zoom out**: Ctrl+- (Windows) or Cmd+- (Mac)
- **Reset**: Ctrl+0 (Windows) or Cmd+0 (Mac)

---

### File Upload Issues

**Q: I can't upload my image**
A: Check:
1. File format is PNG, JPG, GIF, or WEBP
2. File size is less than 5MB
3. The `static/uploads/` folder exists

**Q: My image upload fails with "no error message"**
A: Try:
1. Refresh the browser
2. Use a smaller image
3. Use a different format (try JPG)

**Q: Where are uploaded images stored?**
A: In the `static/uploads/` folder. You can access them via:
```
http://127.0.0.1:5050/static/uploads/filename.jpg
```

**Q: Can I delete an uploaded image?**
A: Only Super Admin can delete entire complaints (and their images). Admins can only update status.

---

### Login & Authentication Issues

**Q: I forgot my password**
A: There's no password reset feature. Options:
1. Use demo credentials
2. Create a new student account
3. Have Super Admin delete your account and recreate it

**Q: Login keeps failing**
A: Check:
1. Username is correct (case-sensitive)
2. Password is correct
3. Account exists (demo or registered)
4. No spaces before/after username

**Q: I registered but can't login**
A: Make sure:
1. You use the username (not email)
2. Password matches what you entered
3. Remember passwords are case-sensitive

**Q: Why can't I login with another admin?**
A: Block admins can only be created by Super Admin. If you want to test admin features, use existing demo admin credentials or ask Super Admin to create an account for you.

---

### Database Issues

**Q: Can I use MySQL instead of SQLite?**
A: This would require code changes to `app.py`. For this project, SQLite is built-in and recommended for development.

**Q: How do I backup my database?**
A: Simply copy `instance/cvr.db` to a backup location:
```bash
cp instance/cvr.db instance/cvr.db.backup
```

**Q: Can I export complaints as CSV?**
A: Currently not supported. You'd need to write a script or use SQLite tools to export the data.

**Q: How many complaints can the database store?**
A: SQLite typically handles millions of records well. No practical limit for a college environment.

---

### Customization

**Q: How do I add more blocks?**
A: Edit `cvr_resolve/app.py` and find the `BLOCKS` list near the top:
```python
BLOCKS = [
    'CM Block',
    'Main Block',
    'First Year Block',
    'NEW BLOCK'  # Add here
]
```

**Q: How do I change the app name?**
A: Search and replace "CVR Resolve" with your name in:
- `templates/base.html`
- `templates/layout.html`
- Other templates as needed

**Q: How do I change the maximum file upload size?**
A: Edit `cvr_resolve/app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB instead of 5MB
```

**Q: Can I add more user roles?**
A: Yes, but it requires modifying:
1. Database schema
2. Backend logic
3. Templates and routes
4. This is an advanced customization

---

### Performance Issues

**Q: The app is running slowly**
A: Try:
1. Restart the Flask server
2. Clear browser cache
3. Close other applications using resources
4. Check internet speed

**Q: Charts take forever to load**
A: This is usually a browser issue. Try:
1. Hard refresh (Ctrl+F5)
2. Try a different browser
3. Check your internet connection

**Q: Database queries are slow**
A: For SQLite performance:
1. The database is typically very fast for college-scale data
2. If you have 10,000+ complaints, consider migrating to PostgreSQL
3. Add indexes to frequently queried columns

---

### Deployment Issues

**Q: Can I deploy this to production?**
A: Yes, but you should:
1. Change `debug=False` in `app.py`
2. Use a production WSGI server (Gunicorn)
3. Set up HTTPS/SSL
4. Use PostgreSQL instead of SQLite
5. Configure environment variables for secrets

**Q: What's the easiest way to deploy?**
A: Try Heroku or PythonAnywhere. They support Flask apps with minimal configuration.

**Q: Will my data be safe?**
A: The app includes basic security. For production, ensure:
1. HTTPS is enabled
2. Database backups are regular
3. Server is kept updated
4. Access is restricted to trusted users

---

### Miscellaneous

**Q: Is there a mobile app?**
A: Not yet, but the web app is fully responsive and works great on mobile browsers.

**Q: Can multiple users be logged in simultaneously?**
A: Yes! Each browser session is separate, so multiple people can use the app at the same time.

**Q: What happens if the server crashes?**
A: Just restart it with `python app.py`. Your data is safe in the SQLite database.

**Q: Can I run this on a Raspberry Pi?**
A: Yes! Python and Flask work great on Raspberry Pi. Perfect for learning!

**Q: Is this code open-source?**
A: Yes, feel free to learn from it, modify it, and use it for any purpose.

**Q: Can I resell this code?**
A: You can use it for your institution. Commercial resale might have different considerations based on your jurisdiction.

**Q: How do I report a bug?**
A: Check the troubleshooting section first. If it's truly a bug, you can examine the code in `app.py` and submit a fix.

---

## Troubleshooting Flowchart

```
App won't start?
├─ Python not installed? → Install Python 3.8+
├─ Dependencies not installed? → Run: pip install -r requirements.txt
├─ Port in use? → Change port in app.py (last line)
└─ Database issue? → Delete instance/cvr.db and restart

App starts but pages don't load?
├─ Wrong URL? → Use http://127.0.0.1:5050
├─ CSS/JS not loading? → Make sure you're in cvr_resolve folder
├─ Browser cache? → Hard refresh (Ctrl+F5)
└─ Folder permissions? → Check static/ and instance/ folders exist

Login fails?
├─ Wrong credentials? → Use demo credentials above
├─ Username/email confusion? → Use username, not email
└─ Forgot demo password? → Check this section above

Features not working?
├─ Images not uploading? → Check static/uploads/ folder exists
├─ Admin can't see complaints? → Check block assignments
├─ Charts not showing? → Hard refresh or try different browser
└─ Search not working? → Check spelling and try simpler query

Database issues?
├─ Database locked? → Restart the app
├─ Database empty? → Delete cvr.db, restart app, demo data auto-created
├─ Want to backup? → Copy instance/cvr.db to backup location
└─ Data corruption? → Delete database and start fresh
```

---

## Support Resources

### Built-in Documentation
- **QUICK_START.md**: 60-second setup guide
- **README.md**: Complete feature documentation
- **PROJECT_OVERVIEW.md**: Architecture and design
- **API_DOCUMENTATION.md**: Technical endpoint details
- **PROJECT_COMPLETION_REPORT.md**: What's included

### Code References
- **app.py**: Read inline comments for logic explanation
- **style.css**: CSS variables for easy theme customization
- **main.js**: JavaScript function comments

### External Resources
- **Flask Docs**: https://flask.palletsprojects.com/
- **SQLite Docs**: https://www.sqlite.org/
- **Python Docs**: https://www.python.org/doc/

---

## Still Need Help?

1. **Read the README.md** - Most questions are answered there
2. **Check PROJECT_OVERVIEW.md** - Technical details and architecture
3. **Review app.py** - Source code with helpful comments
4. **Examine error messages** - Flask provides detailed error pages in debug mode

---

## Feedback

If you have suggestions for improving this application or documentation, consider:
1. Adding features to `app.py`
2. Improving CSS in `style.css`
3. Enhancing functionality in JavaScript
4. Updating documentation files

This is a learning project - feel free to experiment, break things, and learn!

---

**Happy troubleshooting! 🎉**
