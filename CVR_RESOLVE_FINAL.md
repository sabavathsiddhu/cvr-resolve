# CVR-Resolve: Complete Campus Complaint Management System
## Professional Edition (Google OAuth Removed)

---

## 🎯 Project Overview

**CVR-Resolve** is a professional-grade, full-stack complaint management system designed for college campuses. Students can raise complaints with photo attachments, and administrators can manage, prioritize, and resolve them efficiently.

### Key Features
✅ **User Roles:** Student, Admin, Super Admin  
✅ **Account Management:** Register & Login  
✅ **Complaint Submission:** With photo/image uploads  
✅ **Complaint Tracking:** Real-time status updates  
✅ **Admin Dashboard:** Block-level complaint management  
✅ **Analytics:** Super Admin dashboard with charts  
✅ **Security:** Password hashing, role-based access control  

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11+
- Windows/Mac/Linux
- Browser (Chrome, Firefox, Safari, Edge)

### Installation (5 minutes)

```bash
# 1. Navigate to project folder
cd c:\Users\sabav\Downloads\cvr_resolve

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r cvr_resolve/requirements.txt

# 5. Run the application
python cvr_resolve/app.py
```

### Access the Application
- **URL:** http://localhost:5050
- **Browser:** Open in Chrome, Firefox, or Edge

---

## 📋 Demo Credentials

| Role | Username | Password | What They Can Do |
|------|----------|----------|------------------|
| **Student** | `student1` | `stud123` | Raise complaints, upload photos, track status |
| **Admin** | `cm_admin` | `admin123` | Manage CM Block complaints, update status |
| **Super Admin** | `superadmin` | `super123` | Manage all complaints, view analytics, create admins |

---

## 📱 User Workflows

### FOR STUDENTS: Raise a Complaint

1. **Login**
   - Go to http://localhost:5050
   - Enter username: `student1`
   - Enter password: `stud123`
   - Click "Sign In"

2. **Submit New Complaint**
   - Click "Raise New Complaint" button
   - Fill form:
     - **Title:** e.g., "Broken AC in Room 204"
     - **Description:** Detailed problem description
     - **Location:** Select block from dropdown
     - **Photo/Image:** (Optional) Upload complaint photo
   - Click "Submit Complaint"

3. **Track Status**
   - Dashboard shows all your complaints
   - View status: Pending → In Progress → Completed
   - Click complaint to see details & remarks from admin

4. **View Complaint Details**
   - Click on any complaint in sidebar
   - See full description, photo, location
   - View admin remarks/updates

---

### FOR ADMINS: Manage Complaints

1. **Login as Admin**
   - Username: `cm_admin`
   - Password: `admin123`
   - Press login

2. **View Assigned Complaints**
   - Dashboard shows only YOUR block (CM Block)
   - See pending and completed complaints

3. **Update Complaint Status**
   - Click on complaint
   - Change status: Pending → In Progress → Completed
   - Add remarks (optional)
   - Click "Update"

4. **Search & Filter**
   - Filter by status (Pending/Completed/In Progress)
   - Search by title or keywords
   - Sort by date or priority

---

### FOR SUPER ADMINS: Full System Control

1. **Login as Super Admin**
   - Username: `superadmin`
   - Password: `super123`

2. **View All Complaints**
   - See ALL campus complaints across ALL blocks
   - Filter by:
     - Block location
     - Status (Pending/In Progress/Completed)
     - Priority level
   - Search by student name or title

3. **Manage Admins**
   - Create new block admins
   - Assign blocks to admins
   - Edit admin details
   - Delete admins

4. **View Analytics**
   - **Pie Charts:**
     - Complaints by block
     - Complaints by status
     - Complaints by priority
   - **Statistics:**
     - Total complaints
     - Pending complaints
     - Completed complaints

5. **Update Any Complaint**
   - Change status globally
   - Add system-wide remarks

---

## 🛠️ Application Structure

```
cvr_resolve/
├── app.py                    # Main Flask application (500+ lines)
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── instance/
│   └── cvr.db               # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   └── style.css        # Dark theme, responsive design
│   ├── js/
│   │   └── main.js          # Interactivity, modals
│   └── uploads/             # Complaint images stored here
└── templates/
    ├── base.html            # Base layout
    ├── layout.html          # Dashboard layout
    ├── login.html           # Login page
    ├── register.html        # Registration page
    ├── student_dashboard.html        # Student view
    ├── new_complaint.html           # Complaint form
    ├── complaint_detail.html        # View full complaint
    ├── admin_dashboard.html         # Admin view
    └── superadmin_dashboard.html    # Super admin view
```

---

## 📊 Database Schema

### Users Table
```
users (id, username, password, role, name, email, assigned_blocks, created_at)
```
- **Roles:** student, admin, superadmin
- **assigned_blocks:** JSON array of blocks (for admins)

### Complaints Table
```
complaints (id, student_id, title, description, image_path, 
            location, status, priority, remarks, duplicate_of, 
            created_at, updated_at)
```
- **Status:** Pending, In Progress, Completed
- **Priority:** Low, Medium, High (auto-assigned based on keywords)
- **image_path:** Stored in static/uploads/

---

## 🔐 Security Features

✅ **Password Hashing:** Werkzeug security  
✅ **Session Management:** Flask-Login  
✅ **Role-Based Access Control:** Decorators on all admin routes  
✅ **File Upload Validation:** Secure filenames, allowed extensions only  
✅ **SQL Injection Prevention:** Parameterized queries  
✅ **CSRF Protection:** Flask built-in  

---

## 📸 Complaint Photo Upload

### Supported Formats
- PNG, JPG, JPEG, GIF, WebP

### Size Limit
- Maximum 5 MB per image

### Security
- Files renamed with timestamp
- Stored in secure `static/uploads/` folder
- Only verified file types allowed

### How to Upload
1. Go to "Raise New Complaint"
2. Fill complaint details
3. Click "Choose File" (Photo field)
4. Select image from computer
5. Submit form - image uploads automatically

---

## 🎨 UI Features

### Dark Professional Theme
- Modern dark blue/gray color scheme
- Responsive design (mobile, tablet, desktop)
- Smooth animations and transitions
- Clear visual hierarchy

### Responsive Components
- Sidebar navigation
- Card-based layout
- Modal dialogs
- Data tables with sorting
- Chart visualizations (Chart.js)

### User Experience
- Auto-save drafts (in-browser storage)
- Real-time feedback messages
- Intuitive navigation
- Clear call-to-action buttons

---

## 🔧 Technical Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Flask 2.3+ (Python) |
| **Database** | SQLite 3 |
| **Authentication** | Flask-Login + Werkzeug |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Styling** | CSS Grid, Flexbox, Dark Theme |
| **Charts** | Chart.js 4.4 |
| **Security** | Password hashing, RBAC |

---

## 📋 API Routes (25+)

### Public Routes
```
GET  /                          # Index redirect
GET  /login                      # Login form
POST /login                      # Process login
GET  /register                   # Registration form
POST /register                   # Create new student account
GET  /logout                     # Logout (protected)
```

### Student Routes (Protected)
```
GET  /dashboard                  # Dashboard redirect
GET  /student                    # Student dashboard
GET  /student/complaint/new      # New complaint form
POST /student/complaint/new      # Submit complaint
GET  /student/complaint/<id>     # View complaint details
```

### Admin Routes (Protected)
```
GET  /admin                      # Admin dashboard
POST /admin/complaint/<id>/update # Update complaint status
```

### Super Admin Routes (Protected)
```
GET  /superadmin                           # Super admin dashboard
POST /superadmin/admin/new                 # Create new admin
POST /superadmin/admin/<id>/edit           # Edit admin
POST /superadmin/admin/<id>/delete         # Delete admin
POST /superadmin/complaint/<id>/update     # Update complaint
POST /superadmin/complaint/<id>/delete     # Delete complaint
```

---

## 🎓 Sample Data (Auto-Loaded)

### Seeded Admins
- **cm_admin** (CM Block)
- **main_admin** (Main Block)
- **fy_admin** (First Year Block)
- **lab_admin** (Labs & Library Blocks)

### Seeded Students
- **student1** (Rahul Sharma)
- **student2** (Priya Reddy)

### Sample Complaints
- Broken AC in CM Block
- Water leakage in Labs
- Broken projector in Main Block
- WiFi down in Library
- Damaged benches in First Year Block

---

## ⚙️ Configuration Options

### Change Port
In `app.py`, last line:
```python
app.run(debug=False, host='0.0.0.0', port=8080)  # Change 5050 to 8080
```

### Add New Blocks
In `app.py`, line ~25:
```python
BLOCKS = ['CM Block', 'Main Block', 'First Year Block', 'Library Block', 
          'Hostel Block', 'Labs Block', 'Sports Block', 'Canteen Block']
# Add more: 'Your New Block'
```

### Modify Priority Keywords
In `app.py`, function `assign_priority()`:
```python
def assign_priority(description):
    high_keywords = ['broken', 'urgent', 'emergency', ...]
    low_keywords = ['minor', 'small', 'suggest', ...]
```

---

## 🐛 Troubleshooting

### App won't start
```bash
# Solution 1: Ensure virtual environment is active
venv\Scripts\activate

# Solution 2: Reinstall dependencies
pip install -r cvr_resolve/requirements.txt

# Solution 3: Check Python version
python --version  # Must be 3.11+
```

### Database errors
```bash
# Solution: Delete and recreate database
rm cvr_resolve/instance/cvr.db
python cvr_resolve/app.py

# App will auto-create database with sample data
```

### Can't upload images
```bash
# Check folder permissions
# Create uploads folder if missing:
mkdir cvr_resolve/static/uploads
```

### Login not working
- Verify username spelling
- Check password (case-sensitive)
- Use demo credentials first
- Try creating new account

### Port already in use
```bash
# Use different port in app.py:
app.run(debug=False, host='0.0.0.0', port=8080)
```

---

## 📈 Performance Tips

### Speed up application
1. Close unnecessary browser tabs
2. Clear browser cache: `Ctrl+Shift+Delete`
3. Use latest Python 3.11+
4. Run on SSD (faster than HDD)

### Database optimization
1. Keep database size under 100 MB
2. Archive old resolved complaints
3. Export and backup regularly

---

## 🚀 Deployment

### Test Locally First
```bash
python cvr_resolve/app.py
# Visit http://localhost:5050
# Test all features
```

### Deploy to PythonAnywhere
See `PYTHONANYWHERE_DEPLOYMENT.md` for step-by-step guide

### Deploy to Heroku
See `DEPLOYMENT_GUIDE.md` for complete instructions

### Deploy to Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5050
CMD ["python", "app.py"]
```

---

## 📞 Support

### Common Questions

**Q: Can I change admin permissions?**
A: Yes, Super Admin can edit admin details and assign blocks

**Q: How do I backup complaints?**
A: Export the database or copy `instance/cvr.db`

**Q: Can I add more students?**
A: Yes, use the Register page for self-signup

**Q: How do I clear all complaints?**
A: Super Admin can delete from dashboard

**Q: Can admins see other blocks?**
A: No, each admin only sees their assigned blocks

---

## 👥 Team Credits

- **Application:** CVR-Resolve Complaint Management System
- **Framework:** Flask + SQLite
- **Deployed:** PythonAnywhere / Heroku / Docker
- **Students:** For College Campus Management

---

## 📝 Sample Complaint Text

For testing the photo upload:
```
Title: Broken AC in Room 204
Description: The AC unit in room 204 is not working since yesterday. 
             Students cannot study due to heat. Please fix urgently.
Location: CM Block
Photo: Screenshot of AC or room photo
```

---

## ✅ Testing Checklist

Use this to verify all features work:

**User Registration & Login**
- [ ] Can register new student account
- [ ] Can login with new account
- [ ] Can login with demo credentials
- [ ] Can logout

**Student Features**
- [ ] Can view student dashboard
- [ ] Can navigate to raise complaint
- [ ] Can submit complaint without photo
- [ ] Can submit complaint with photo
- [ ] Can view own complaints
- [ ] Can see complaint details
- [ ] Can switch between complaints

**Admin Features**
- [ ] Can login as admin
- [ ] Can see only assigned block complaints
- [ ] Can update complaint status
- [ ] Can add remarks
- [ ] Can search complaints
- [ ] Can filter by status

**Super Admin Features**
- [ ] Can login as super admin
- [ ] Can see all complaints
- [ ] Can view analytics charts
- [ ] Can create new admin
- [ ] Can edit admin details
- [ ] Can delete admin
- [ ] Can delete complaint

**Photo Upload**
- [ ] Can select PNG/JPG image
- [ ] Upload shows in complaint
- [ ] Can view uploaded photo
- [ ] Files stored in correct location

---

## 🎉 You're Ready!

Your professional complaint management system is complete and ready to use!

**Run the app:**
```bash
python cvr_resolve/app.py
```

**Visit:** http://localhost:5050

**Login with:** student1 / stud123

**Happy complaining! 😊**
