# 📚 CVR Resolve - Installation & Quick Start Guide

## ⚡ 60-Second Quick Start

### Windows (PowerShell)
```powershell
# Navigate to project
cd c:\Users\sabav\Downloads\cvr_resolve

# Create venv (one time)
python -m venv .venv

# Activate venv (every session)
.\.venv\Scripts\Activate.ps1

# Install dependencies (one time)
pip install -r cvr_resolve\requirements.txt

# Run the app
cd cvr_resolve
python app.py
```

### macOS/Linux
```bash
cd ~/cvr_resolve

python -m venv .venv
source .venv/bin/activate

pip install -r cvr_resolve/requirements.txt

cd cvr_resolve
python app.py
```

### 🌐 Open Browser
**http://127.0.0.1:5050**

---

## 🔐 Instant Login (Demo Credentials)

Pick any account below and log in:

```
Super Admin:    superadmin / super123
CM Admin:       cm_admin / admin123
Student:        student1 / stud123
```

Or register a new student account through the UI!

---

## 🎯 What You Can Do

### 🎓 As a Student:
1. Login with `student1 / stud123`
2. Click "New Complaint"
3. Fill in title, location, description
4. Upload an optional image
5. Click "Submit Complaint"
6. View your complaints on the dashboard
7. Watch for admin updates!

### 👨‍💼 As a Block Admin:
1. Login with `cm_admin / admin123`
2. See all complaints from CM Block
3. Click "Update" on any complaint
4. Change status to "Completed"
5. Add remarks for the student
6. Check your stats at top

### 👨‍✈️ As Super Admin:
1. Login with `superadmin / super123`
2. View ALL complaints from all blocks
3. See interactive charts showing:
   - Complaints per block (bar chart)
   - Pending vs Completed (doughnut)
   - Priority distribution (doughnut)
4. Create/edit/delete block admins
5. Manage all system data

---

## 📂 File Structure

```
cvr_resolve/
├── app.py                   ← Main Flask Application
├── requirements.txt         ← Python Dependencies
├── instance/
│   └── cvr.db              ← Database (auto-created)
├── static/
│   ├── css/style.css       ← Styling
│   ├── js/main.js          ← Interactivity
│   └── uploads/            ← Complaint images
└── templates/
    ├── base.html
    ├── layout.html
    ├── login.html
    ├── register.html
    ├── student_dashboard.html
    ├── new_complaint.html
    ├── complaint_detail.html
    ├── admin_dashboard.html
    └── superadmin_dashboard.html
```

---

## ✨ Features At a Glance

✅ **Role-Based Access**: Student → Admin → Super Admin
✅ **Complaint Submission**: With title, description, image upload, location
✅ **Duplicate Detection**: Automatically flags similar complaints
✅ **Smart Priority**: Keywords auto-assign High/Medium/Low priorities
✅ **Status Tracking**: Pending → Completed with admin remarks
✅ **Block Management**: Admins see only their assigned blocks
✅ **Analytics**: Super Admin dashboard with 3 interactive charts
✅ **Dark Theme**: Beautiful, modern, responsive UI
✅ **Search & Filter**: Find complaints quickly
✅ **Mobile Friendly**: Works on phones, tablets, desktops

---

## 🔍 Example Workflows

### Workflow 1: Student Submits Complaint
1. Student logs in
2. Clicks "New Complaint"
3. Types "Broken AC in Room 204"
4. Selects "CM Block" and describes the issue
5. Uploads a photo
6. System auto-assigns "High" priority (keyword: "broken")
7. System checks for duplicates
8. Complaint created! Student sees notification

### Workflow 2: Admin Reviews & Updates
1. Admin logs in
2. Dashboard shows all CM Block complaints
3. Finds the complaint about broken AC
4. Clicks "Update"
5. Changes status to "Completed"
6. Adds remark: "AC unit replaced on March 10"
7. Student immediately sees the update!

### Workflow 3: Super Admin Analytics
1. Super Admin logs in
2. Sees system-wide stats:
   - 47 total complaints this month
   - 12 still pending
   - 35 resolved
3. Views charts:
   - CM Block: 8 complaints (highest)
   - Labs: 12 complaints (but 11 resolved!)
   - First Year: 5 complaints (all pending)
4. Decides to allocate more resources to First Year block
5. Creates new admin for First Year block

---

## 🛠️ Common Commands

### Reset Database
Remove `instance/cvr.db` file:
```bash
rm instance/cvr.db
```
App will create fresh database on next run.

### Change Port (if 5050 is busy)
Edit `app.py`, change last line:
```python
app.run(debug=True, port=5051)  # Use 5051 instead
```

### Add More Blocks
Edit `app.py`, find `BLOCKS` list:
```python
BLOCKS = [
    'CM Block', 'Main Block', 'First Year Block',
    'YOUR_NEW_BLOCK'  # Add here
]
```

### Increase Upload File Size
Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
```

---

## 🐛 Troubleshooting

**Q: Port 5050 already in use?**
A: Change port number in app.py (last line) or kill the process using the port

**Q: Can't find database?**
A: Run app once to auto-create `instance/cvr.db`

**Q: Images not uploading?**
A: Verify `static/uploads/` folder exists and is writable

**Q: Students can't login after registration?**
A: Check if username already exists (must be unique)

**Q: Admin only sees some blocks?**
A: Super Admin assigns blocks to admins - check admin's assigned blocks

---

## 🚀 Next Steps

1. **Play Around**: Use demo accounts to explore all features
2. **Test Different Roles**: See what each role can do
3. **Submit Complaints**: Test the student workflow
4. **Manage Complaints**: Update status as admin
5. **View Analytics**: Check super admin dashboard
6. **Create Admins**: Test super admin management features
7. **Read Full Docs**: Check README.md for detailed documentation

---

## 📞 Support

- **Default Port**: 5050
- **Database**: SQLite (instance/cvr.db)
- **Images Stored**: static/uploads/
- **Python Required**: 3.8+

**Good luck! 🎉**
