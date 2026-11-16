from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import mysql.connector

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change_this_secret_key")

# Admin login (set ADMIN_USER / ADMIN_PASSWORD env variables to override)
ADMIN_USER = os.environ.get("ADMIN_USER", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", ""),
    database="placement"
)
cursor = db.cursor(dictionary=True)

# ------------------------- Home Page -------------------------
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/home/com')
def home_com():
    return render_template('company.html')

# ------------------------- Login/Logout -------------------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            session['admin'] = username
            flash("Login successful!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid login", "danger")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("login"))

# ------------------------- Student Registration -------------------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        student_id = request.form['studentid']
        name = request.form['name']
        phone = request.form['phone']
        department = request.form['department']
        graduation_year = request.form['year']
        company = request.form['company']

        # 1. Get drive_id from the company name
        cursor.execute("SELECT drive_id FROM drives WHERE company_name = %s", (company,))
        drive_result = cursor.fetchone()
        if not drive_result:
            flash("Invalid company name selected", "danger")
            return redirect(url_for('register'))
        drive_id = drive_result['drive_id']

        status = "Registered"

        # 2. Insert into placement_registration (student profile)
        cursor.execute("""
            INSERT INTO placement_registration 
            (student_id, name, phone, department, graduation_year, company, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (student_id, name, phone, department, graduation_year, company, status))

        # 3. Insert into registrations (drive registration)
        cursor.execute("""
            INSERT INTO registrations (student_id, drive_id, status, registration_date)
            VALUES (%s, %s, %s, NOW())
        """, (student_id, drive_id, status))

        db.commit()
        flash("Registered successfully!", "success")
        return redirect(url_for('home'))

    return render_template("register.html")

# ------------------------- Student Check -------------------------
@app.route('/student_check', methods=['GET','POST'])
def student_check():
    if request.method == 'POST':
        student_id = request.form['student_id']
        cursor.execute("SELECT * FROM placement_registration WHERE student_id=%s", (student_id,))
        student = cursor.fetchone()
        if student:
            return redirect(url_for('student_options', student_id=student_id))
        else:
            flash("Invalid Registration ID", "danger")
    return render_template("student_check.html")

# ------------------------- Student Options -------------------------
@app.route('/student/options/<student_id>')
def student_options(student_id):
    cursor.execute("SELECT * FROM placement_registration WHERE student_id=%s", (student_id,))
    student = cursor.fetchone()
    if student:
        return render_template("student_options.html", student=student)
    else:
        flash("Student ID not found", "danger")
        return redirect(url_for("student_check"))

# ------------------------- View Student -------------------------
@app.route('/student/view/<student_id>')
def student_view(student_id):
    cursor.execute("SELECT * FROM placement_registration WHERE student_id=%s", (student_id,))
    student = cursor.fetchone()
    if student:
        return render_template("student_view.html", student=student)
    else:
        flash("Student not found", "danger")
        return redirect(url_for("student_check"))

# ------------------------- Edit Student -------------------------
@app.route('/student/edit/<student_id>', methods=['GET','POST'])
def student_edit(student_id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        department = request.form['department']
        graduation_year = request.form['graduation_year']
        company = request.form['company']

        cursor.execute("""
            UPDATE placement_registration
            SET name=%s, phone=%s, department=%s, graduation_year=%s, company=%s
            WHERE student_id=%s
        """, (name, phone, department, graduation_year, company, student_id))
        db.commit()
        flash("Updated successfully!", "success")
        return redirect(url_for('student_options', student_id=student_id))

    cursor.execute("SELECT * FROM placement_registration WHERE student_id=%s", (student_id,))
    student = cursor.fetchone()
    if student:
        return render_template("student_edit.html", student=student)
    else:
        flash("Student not found", "danger")
        return redirect(url_for("student_check"))

# ------------------------- Student Status -------------------------
@app.route('/student/status/<student_id>')
def student_status(student_id):
    cursor.execute("SELECT * FROM placement_registration WHERE student_id=%s", (student_id,))
    student = cursor.fetchone()
    if student:
        return render_template("student_status.html", student=student, status=student['status'])
    else:
        flash("Student not found", "danger")
        return redirect(url_for("student_check"))

# ------------------------- Admin Dashboard with Registration Count -------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' not in session:
        flash("Login required", "danger")
        return redirect(url_for('login'))

    # Add new drive
    if request.method == 'POST':
        company_name = request.form['company_name']
        drive_date = request.form['drive_date']
        location = request.form.get('location')
        package_details = request.form.get('package_details')
        eligibility = request.form['eligibility']
        description = request.form.get('description')

        cursor.execute("""
            INSERT INTO drives 
            (company_name, drive_date, location, package_details, eligibility, description)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (company_name, drive_date, location, package_details, eligibility, description))
        db.commit()
        flash("Drive added successfully", "success")
        return redirect(url_for('admin_dashboard'))

    # ✅ Get drives with count of student registrations
    # ✅ Get drives with registration counts
    cursor.execute("""
    SELECT d.*, 
           COUNT(r.reg_id) AS registration_count
    FROM drives d
    LEFT JOIN registrations r ON d.drive_id = r.drive_id
    GROUP BY d.drive_id
""")
    drives = cursor.fetchall()


    # Get all student registrations
    cursor.execute("""
        SELECT r.reg_id, r.student_id, r.status, r.notes, r.registration_date,
               pr.name AS student_name,
               d.company_name
        FROM registrations r
        LEFT JOIN placement_registration pr ON r.student_id = pr.student_id
        LEFT JOIN drives d ON r.drive_id = d.drive_id
        ORDER BY r.registration_date DESC
    """)
    registrations = cursor.fetchall()

    # Status summary
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN status = 'Registered' THEN 1 ELSE 0 END) AS registered,
            SUM(CASE WHEN status = 'Placed' THEN 1 ELSE 0 END) AS placed,
            SUM(CASE WHEN status = 'Not Placed' THEN 1 ELSE 0 END) AS not_placed
        FROM placement_registration
    """)
    status_counts = cursor.fetchone() or {
        'registered': 0,
        'placed': 0,
        'not_placed': 0,
    }

    return render_template("admin.html",
                           drives=drives,
                           registrations=registrations,
                           registered_count=status_counts['registered'],
                           placed_count=status_counts['placed'],
                           not_placed_count=status_counts['not_placed'])

# ------------------------- Delete Drive -------------------------
@app.route('/delete_drive/<int:drive_id>', methods=['POST'])
def delete_drive(drive_id):
    cursor.execute("SELECT COUNT(*) as cnt FROM registrations WHERE drive_id=%s", (drive_id,))
    result = cursor.fetchone()
    if result['cnt'] == 0:
        cursor.execute("DELETE FROM drives WHERE drive_id=%s", (drive_id,))
        db.commit()
        flash("Drive deleted", "success")
    else:
        flash("Cannot delete. Students registered for this drive.", "danger")
    return redirect(url_for('admin_dashboard'))

# ------------------------- Update Registration Status -------------------------
@app.route('/update_status/<int:reg_id>', methods=['POST'])
def update_status(reg_id):
    status = request.form.get('status')
    notes = request.form.get('notes')

    cursor.execute("""
        SELECT student_id FROM registrations WHERE reg_id=%s
    """, (reg_id,))
    registration = cursor.fetchone()

    if not registration:
        flash("Registration not found", "danger")
        return redirect(url_for('admin_dashboard'))

    cursor.execute("""
        UPDATE registrations SET status=%s, notes=%s WHERE reg_id=%s
    """, (status, notes, reg_id))
    cursor.execute("""
        UPDATE placement_registration
        SET status=%s
        WHERE student_id=%s
    """, (status, registration['student_id']))
    db.commit()
    flash("Status updated", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/placement_details/<int:reg_id>', methods=['GET', 'POST'])
def placement_details(reg_id):
    if request.method == 'POST':
        role = request.form.get('role')
        timing = request.form.get('timing')

        cursor.execute("""
            SELECT student_id FROM registrations WHERE reg_id = %s
        """, (reg_id,))
        registration = cursor.fetchone()

        if not registration:
            flash("Registration not found", "danger")
            return redirect(url_for('admin_dashboard'))

        cursor.execute("""
            UPDATE placement_registration
            SET role=%s, timing=%s
            WHERE student_id=%s
        """, (role, timing, registration['student_id']))
        db.commit()
        flash("Placement details updated!", "success")
        return redirect(url_for('admin_dashboard'))

    cursor.execute("""
        SELECT r.reg_id, r.student_id, r.status,
               p.name, p.department, p.company, p.role, p.timing
        FROM registrations r
        LEFT JOIN placement_registration p ON r.student_id = p.student_id
        WHERE r.reg_id = %s
    """, (reg_id,))
    student = cursor.fetchone()
    return render_template("placement_details.html", student=student)


@app.route("/about")
def about():
    return render_template("about.html")




# ------------------------- Main -------------------------
if __name__ == '__main__':
    app.run(debug=True)
