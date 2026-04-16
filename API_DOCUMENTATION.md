# 🔌 CVR Resolve - API Documentation

## Overview

CVR Resolve provides a complete REST-like API for complaint management. All endpoints are protected with authentication and role-based access control.

**Base URL**: `http://127.0.0.1:5050`

---

## Authentication

### Login Endpoint
```http
POST /login
```

**Parameters** (Form Data):
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Response** (Success - 302 Redirect):
```
Location: /dashboard
Set-Cookie: session=...
```

**Response** (Failure - 200 with error message):
```
Rendered login.html with error flash message
```

**Demo Credentials**:
- Super Admin: `superadmin` / `super123`
- Admin: `cm_admin` / `admin123`
- Student: `student1` / `stud123`

---

## User Management

### Register (Students Only)
```http
GET /register
```
**Response**: Registration form HTML

```http
POST /register
```

**Parameters** (Form Data):
```json
{
  "username": "string (required, unique)",
  "password": "string (required)",
  "name": "string (required)",
  "email": "string (optional)"
}
```

**Response** (Success - 302 Redirect):
```
Location: /login
Message: "Account created! Please login."
```

**Response** (Failure):
```
Message: "Username already exists." or "All fields required."
```

### Logout
```http
GET /logout
Required: Authentication + Any Role
```

**Response**:
```
Redirect: /login
Message: "Logged out successfully."
```

---

## Dashboard Routes

### General Dashboard Redirect
```http
GET /dashboard
Required: Authentication
```

**Logic**:
- Student role → `/student`
- Admin role → `/admin`
- Super Admin role → `/superadmin`

---

## Student Routes

### Student Dashboard
```http
GET /student
Required: Authentication + Role: student
```

**Response**: HTML page with:
```json
{
  "complaints": [
    {
      "id": "number",
      "title": "string",
      "description": "string",
      "location": "string",
      "status": "Pending|Completed",
      "priority": "High|Medium|Low",
      "image_path": "string|null",
      "remarks": "string|null",
      "duplicate_of": "number|null",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
  ],
  "stats": {
    "total": "number",
    "pending": "number",
    "completed": "number"
  }
}
```

### Get Complaint Submission Form
```http
GET /student/complaint/new
Required: Authentication + Role: student
```

**Response**: HTML form with:
- Text input: title
- Textarea: description (required)
- Select: location (from predefined blocks)
- File input: image (optional)

### Submit New Complaint
```http
POST /student/complaint/new
Required: Authentication + Role: student
Content-Type: multipart/form-data
```

**Parameters**:
```json
{
  "title": "string (required)",
  "description": "string (required)",
  "location": "string (required, must be from BLOCKS list)",
  "image": "file (optional, max 5MB, PNG|JPG|GIF|WEBP)"
}
```

**Server-Side Processing**:
1. Validates all required fields
2. Saves image to `/static/uploads/` if provided
3. Auto-detects duplicate complaints
4. Auto-assigns priority based on keywords
5. Creates complaint record

**Response** (Success):
```json
{
  "success": true,
  "message": "Complaint submitted successfully!",
  "complaint_id": "number"
}
```

If duplicate found:
```
Message: "Complaint submitted! Note: A similar complaint (#n) already exists."
```

**Response** (Failure):
```json
{
  "error": "Field validation message"
}
```

### View Complaint Details
```http
GET /student/complaint/<complaint_id>
Required: Authentication + Role: student + Ownership of complaint
```

**Response**: HTML page with:
```json
{
  "complaint": {
    "id": "number",
    "title": "string",
    "description": "string",
    "location": "string",
    "status": "Pending|Completed",
    "priority": "High|Medium|Low",
    "image_path": "string|null",
    "remarks": "string|null",
    "duplicate_of": "number|null",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
}
```

---

## Admin Routes

### Admin Dashboard
```http
GET /admin
Required: Authentication + Role: admin
```

**Query Parameters**:
```
?block=<block_name>         # Filter by specific block
?status=<Pending|Completed> # Filter by status
?search=<query>             # Search title/description
```

**Response**: HTML page with:
```json
{
  "complaints": [
    {
      "id": "number",
      "title": "string",
      "description": "string",
      "location": "string (must be in assigned_blocks)",
      "status": "Pending|Completed",
      "priority": "High|Medium|Low",
      "student_name": "string",
      "remarks": "string|null",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
  ],
  "stats": {
    "total": "number (from assigned blocks only)",
    "pending": "number",
    "completed": "number"
  },
  "assigned_blocks": ["array of block names"]
}
```

**Access Control**:
- Admin can only see complaints from assigned blocks
- Filtering constraints applied by location

### Update Complaint Status & Remarks
```http
POST /admin/complaint/<complaint_id>/update
Required: Authentication + Role: admin + Block access
Content-Type: application/x-www-form-urlencoded
```

**Parameters**:
```json
{
  "status": "Pending|Completed (required)",
  "remarks": "string (optional)"
}
```

**Server-Side Validation**:
1. Verify admin is authenticated
2. Verify complaint exists
3. Verify complaint is in admin's assigned blocks
4. Update status and remarks
5. Set updated_at timestamp

**Response** (Success):
```
Redirect: /admin
Message: "Complaint updated successfully!"
```

**Response** (Failure - No Access):
```
Redirect: /admin
Message: "Access denied."
```

---

## Super Admin Routes

### Super Admin Dashboard
```http
GET /superadmin
Required: Authentication + Role: superadmin
```

**Query Parameters**:
```
?block=<block_name>         # Filter by block
?status=<Pending|Completed> # Filter by status
?search=<query>             # Search by title/student name
```

**Response**: Complete system data:
```json
{
  "complaints": [
    {
      "id": "number",
      "title": "string",
      "student_name": "string",
      "location": "string",
      "status": "Pending|Completed",
      "priority": "High|Medium|Low",
      "created_at": "timestamp"
    }
  ],
  "admins": [
    {
      "id": "number",
      "name": "string",
      "username": "string",
      "email": "string",
      "assigned_blocks": "JSON array"
    }
  ],
  "stats": {
    "total": "number (all complaints)",
    "pending": "number",
    "completed": "number",
    "total_all": "number (for unfiltered stats)"
  },
  "block_chart": {"Block Name": complaint_count, ...},
  "status_chart": {"Pending": count, "Completed": count},
  "priority_chart": {"High": count, "Medium": count, "Low": count}
}
```

### Create Block Admin
```http
POST /superadmin/admin/new
Required: Authentication + Role: superadmin
Content-Type: application/x-www-form-urlencoded
```

**Parameters**:
```json
{
  "username": "string (required, unique)",
  "password": "string (required)",
  "name": "string (required)",
  "email": "string (optional)",
  "blocks": ["array of block names (required)"]
}
```

**Request Example**:
```
POST /superadmin/admin/new
username=library_admin
password=admin456
name=Library Block Admin
email=library@cvr.ac.in
blocks=Library+Block
blocks=Reading+Room
```

**Response** (Success):
```
Redirect: /superadmin
Message: "Admin "name" created successfully!"
```

**Response** (Failure - Username exists):
```
Message: "Username already exists."
```

### Edit Block Admin
```http
POST /superadmin/admin/<admin_id>/edit
Required: Authentication + Role: superadmin
Content-Type: application/x-www-form-urlencoded
```

**Parameters**:
```json
{
  "name": "string (required)",
  "email": "string (optional)",
  "blocks": ["array of block names (required)"]
}
```

**Response**:
```
Redirect: /superadmin
Message: "Admin updated."
```

### Delete Block Admin
```http
POST /superadmin/admin/<admin_id>/delete
Required: Authentication + Role: superadmin
```

**Response**:
```
Redirect: /superadmin
Message: "Admin deleted."
```

### Update Any Complaint (Super Admin)
```http
POST /superadmin/complaint/<complaint_id>/update
Required: Authentication + Role: superadmin
Content-Type: application/x-www-form-urlencoded
```

**Parameters**:
```json
{
  "status": "Pending|Completed (required)",
  "remarks": "string (optional)"
}
```

**Response**:
```
Redirect: /superadmin
Message: "Complaint updated."
```

### Delete Complaint
```http
POST /superadmin/complaint/<complaint_id>/delete
Required: Authentication + Role: superadmin
```

**Server-Side Processing**:
1. Retrieve complaint
2. Delete associated image file (if exists)
3. Delete complaint record
4. Return success message

**Response**:
```
Redirect: /superadmin
Message: "Complaint deleted."
```

---

## Error Responses

### Unauthorized (Not Authenticated)
```http
302 Redirect /login
```

### Forbidden (Wrong Role)
```http
302 Redirect /dashboard
Message: "Access denied."
```

### Not Found
```http
404 Default Flask 404 page
```

### Validation Error
```http
200 (with form re-rendered)
Message: "Specific validation message"
```

---

## Data Models

### User Object
```json
{
  "id": "number",
  "username": "string",
  "password": "string (hashed)",
  "role": "student|admin|superadmin",
  "name": "string",
  "email": "string|null",
  "assigned_blocks": "JSON array|empty for students",
  "created_at": "timestamp"
}
```

### Complaint Object
```json
{
  "id": "number",
  "student_id": "number (FK: users.id)",
  "title": "string",
  "description": "string",
  "image_path": "string|null (filename only)",
  "location": "string (block name)",
  "status": "Pending|Completed",
  "priority": "High|Medium|Low",
  "remarks": "string|null",
  "duplicate_of": "number|null (complaint ID)",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

---

## Available Blocks

```
CM Block
Main Block
First Year Block
Library Block
Hostel Block
Labs Block
Sports Block
Canteen Block
```

---

## Priority Assignment Rules

Complaint priority is auto-assigned based on keywords in description:

**HIGH** (any of these keywords):
- "broken"
- "urgent"
- "emergency"
- "not working"
- "damaged"
- "leak"
- "fire"
- "danger"

**LOW** (any of these keywords):
- "minor"
- "small"
- "suggest"
- "request"
- "paint"

**MEDIUM**: Default (no high/low keywords)

---

## Duplicate Detection Algorithm

When a complaint is submitted:

1. Query database for pending complaints in same location
2. Check if first 20 characters of new description match existing complaints (case-insensitive)
3. If match found:
   - Flag with warning badge
   - Store `duplicate_of` reference
   - Display message to student
4. If no match, proceed normally

---

## Image Upload Specifications

**Endpoint**: File input in `/student/complaint/new` form

**Allowed Formats**:
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)

**Constraints**:
- Maximum file size: 5 MB
- All files: `content_type` enforced
- Saved to: `/static/uploads/`
- Filename: `{timestamp}_{original_filename}`

**Storage Examples**:
```
static/uploads/1710098123.456_broken_ac.jpg
static/uploads/1710098234.789_water_leak.png
```

**Access URL**:
```
/static/uploads/1710098123.456_broken_ac.jpg
```

---

## Session Management

### Session Data
```json
{
  "user_id": "number",
  "username": "string",
  "role": "string",
  "name": "string",
  "assigned_blocks": "array"
}
```

### Session Lifetime
- Persists during browser session
- Expires on browser close or 30+ minutes idle
- Can be manually cleared with `/logout`

### Cookies
- `session`: Encrypted Flask session cookie
- Secure by default in Flask-Login

---

## Rate Limiting

Currently **NOT implemented**. For production, add:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

# Apply to endpoints:
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    ...
```

---

## CORS Policy

Currently **NOT enabled** (same-origin only). For cross-origin requests, add:
```python
from flask_cors import CORS
CORS(app)
```

---

## Performance Notes

### Query Optimization
- Most queries return in <10ms
- Aggregation queries (analytics) optimized with GROUP BY
- Consider adding indexes for production

### Caching
- Not currently implemented
- Consider Redis for session/page caching

### File Uploads
- Images stored on disk, not in database
- Path stored as filename for easy retrieval
- Consider S3/CDN for production

---

## Testing with cURL

### Login
```bash
curl -X POST http://127.0.0.1:5050/login \
  -d "username=student1&password=stud123" \
  -c cookies.txt
```

### Submit Complaint
```bash
curl -X POST http://127.0.0.1:5050/student/complaint/new \
  -b cookies.txt \
  -F "title=Broken AC" \
  -F "description=AC not working in room 204" \
  -F "location=CM Block" \
  -F "image=@/path/to/image.jpg"
```

### View Dashboard
```bash
curl http://127.0.0.1:5050/student \
  -b cookies.txt
```

---

## Common Use Cases

### Scenario 1: New Student Registration & First Complaint
```
1. POST /register (create account)
2. POST /login (authenticate)
3. POST /student/complaint/new (submit complaint)
4. GET /student/complaint/<id> (view details)
```

### Scenario 2: Admin Reviews & Updates
```
1. POST /login (authenticate as admin)
2. GET /admin (view dashboard)
3. POST /admin/complaint/<id>/update (mark as completed)
```

### Scenario 3: Super Admin Analytics
```
1. POST /login (authenticate as superadmin)
2. GET /superadmin (view full dashboard with charts)
3. POST /superadmin/admin/new (create new admin)
```

---

## Response Time SLO (Service Level Objectives)

| Endpoint | Target | Notes |
|----------|--------|-------|
| Login | <100ms | Auth + DB query |
| Dashboard Load | <500ms | Page render + data |
| Submit Complaint | <1000ms | File upload + processing |
| Admin Update | <200ms | DB update |
| Charts Render | <1500ms | Data fetch + JS render |

---

## API Versioning

**Current Version**: 1.0 (No versioning prefix)

Future versions might use:
- `/api/v2/complaints`
- `/api/v2/users`

---

## Change Log

### Version 1.0 (Current)
- ✅ Complete CRUD for complaints
- ✅ User authentication and RBAC
- ✅ Admin management
- ✅ Analytics dashboard
- ✅ File uploads
- ✅ Duplicate detection
- ✅ Priority assignment

---

## Support

For API issues or questions, refer to:
- Main README.md for features
- app.py source code for implementation details
- QUICK_START.md for setup issues

