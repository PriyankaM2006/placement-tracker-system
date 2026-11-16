# Placement Tracker System

A Flask web application that helps a college manage campus placements. Students can register for company placement drives and track their status, while an admin manages drives, updates registration status, and monitors placement numbers from a dashboard.

## Features

### Student side
- Register for a placement drive (Student ID, name, phone, department, graduation year, company)
- Log in with the Student ID to **view**, **edit**, or **check status** of the registration
- Browse top recruiting companies

### Admin side
- Secure admin login (session based)
- Add and delete placement drives (company, date, location, package, eligibility, description)
- See the number of registrations for each drive
- Update each student's status (Registered / Placed / Not Placed) with notes
- Add placement details (role and timing) for placed students
- Dashboard summary of Registered, Placed and Not Placed counts

## Tech Stack
- **Backend:** Python, Flask
- **Database:** MySQL (`mysql-connector-python`)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap, Jinja2 templates

## Project Structure
```
placement-tracker-system/
├── app.py               # Flask routes and database logic
├── database.sql         # MySQL schema
├── requirements.txt
├── static/
│   └── images/          # Logos and page images
└── templates/
    ├── home.html
    ├── about.html
    ├── company.html
    ├── register.html
    ├── login.html
    ├── admin.html
    ├── placement_details.html
    ├── student_check.html
    ├── student_options.html
    ├── student_view.html
    ├── student_edit.html
    └── student_status.html
```

## Getting Started

### Prerequisites
- Python 3.8+
- MySQL Server

### 1. Clone the repository
```bash
git clone https://github.com/PriyankaM2006/placement-tracker-system.git
cd placement-tracker-system
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up the database
Open MySQL and run the schema file:
```bash
mysql -u root -p < database.sql
```
This creates the `placement` database and its tables (`users`, `placement_registration`, `drives`, `registrations`).

### 4. Configure credentials
Credentials are read from environment variables, so nothing secret is stored in the code.

Windows (Command Prompt):
```
set DB_PASSWORD=your_mysql_password
```
Windows (PowerShell): `$env:DB_PASSWORD="your_mysql_password"`
Linux/Mac: `export DB_PASSWORD=your_mysql_password`

| Variable | Default | Purpose |
|---|---|---|
| `DB_USER` | `root` | MySQL user |
| `DB_PASSWORD` | *(empty)* | MySQL password |
| `SECRET_KEY` | `change_this_secret_key` | Flask session key |
| `ADMIN_USER` | `admin@example.com` | Admin login |
| `ADMIN_PASSWORD` | `admin123` | Admin password |

### 5. Run the app
```bash
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

## How It Works
1. Admin logs in (default `admin@example.com` / `admin123`) and adds a placement drive for a company.
2. A student registers for that company's drive from the **Register** page.
3. The registration appears in the admin dashboard, where the admin updates the status and notes.
4. The student enters their Student ID in **Student Management** to see the updated status.

## Database Tables
| Table | Purpose |
|---|---|
| `users` | Admin login |
| `placement_registration` | Student profile, current status, role and timing |
| `drives` | Company placement drives |
| `registrations` | Links each student to a drive, with status and notes |

## Future Improvements
- Password hashing and a proper student login
- Search and filter in the admin dashboard
- Export placement reports to Excel/PDF

## Author
**Priyanka M**
[LinkedIn](https://linkedin.com/in/priyanka-m-9358972a7)
