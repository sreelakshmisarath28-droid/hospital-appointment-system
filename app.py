from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hospital_secret_key_2025"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hospital.db')

DEPARTMENTS = ["General", "Cardiology", "Neurology", "Orthopaedic",
               "Paediatric", "Gynaecology", "Dermatology"]

TIME_SLOTS = ["09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM",
              "11:00 AM", "11:30 AM", "12:00 PM", "02:00 PM",
              "02:30 PM", "03:00 PM", "03:30 PM", "04:00 PM"]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---- Smart Scheduling: auto assign best available doctor ----
def smart_assign_doctor(department, appointment_date):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Doctors
                   WHERE DEPARTMENT=?
                   AND CURRENT_PATIENTS < MAX_PATIENTS
                   ORDER BY CURRENT_PATIENTS ASC""", (department,))
    doctors = cur.fetchall()
    conn.close()
    if doctors:
        return dict(doctors[0])
    return None

# ---- Home Page ----
@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as total FROM Appointments")
    total_appointments = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM Doctors")
    total_doctors = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM Appointments WHERE STATUS='Confirmed'")
    confirmed = cur.fetchone()['total']
    cur.execute("SELECT * FROM Appointments ORDER BY APPOINTMENT_ID DESC LIMIT 5")
    recent = cur.fetchall()
    conn.close()
    return render_template('index.html',
                           total_appointments=total_appointments,
                           total_doctors=total_doctors,
                           confirmed=confirmed,
                           recent=recent,
                           departments=DEPARTMENTS)

# ---- Book Appointment ----
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        patient_name    = request.form['patient_name']
        age             = request.form['age']
        gender          = request.form['gender']
        contact         = request.form['contact']
        email           = request.form['email']
        department      = request.form['department']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        symptoms        = request.form['symptoms']

        if not patient_name or not contact or not department or not appointment_date:
            flash("Please fill all required fields!", "danger")
            return redirect(url_for('book'))

        # Smart scheduling — auto assign doctor
        assigned = smart_assign_doctor(department, appointment_date)
        if not assigned:
            flash(f"No doctors available in {department} department. Please choose another date or department.", "warning")
            return redirect(url_for('book'))

        doctor_id   = assigned['DOCTOR_ID']
        doctor_name = assigned['DOCTOR_NAME']
        booked_on   = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO Appointments
            (PATIENT_NAME,AGE,GENDER,CONTACT,EMAIL,DEPARTMENT,DOCTOR_ID,
             DOCTOR_NAME,APPOINTMENT_DATE,APPOINTMENT_TIME,SYMPTOMS,STATUS,BOOKED_ON)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (patient_name, age, gender, contact, email, department,
             doctor_id, doctor_name, appointment_date, appointment_time,
             symptoms, 'Confirmed', booked_on))
        cur.execute("UPDATE Doctors SET CURRENT_PATIENTS=CURRENT_PATIENTS+1 WHERE DOCTOR_ID=?", (doctor_id,))
        conn.commit()
        conn.close()

        flash(f"Appointment booked successfully! Assigned to {doctor_name}", "success")
        return redirect(url_for('appointments'))

    return render_template('book.html', departments=DEPARTMENTS, time_slots=TIME_SLOTS)

# ---- View All Appointments ----
@app.route('/appointments')
def appointments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Appointments ORDER BY APPOINTMENT_ID DESC")
    rows = cur.fetchall()
    conn.close()
    return render_template('appointments.html', appointments=rows)

# ---- Search Appointments ----
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    search_val = ""
    search_by  = ""
    if request.method == 'POST':
        search_by  = request.form['search_by']
        search_val = request.form['search_val']
        col_map = {
            "Patient Name": "PATIENT_NAME",
            "Doctor Name":  "DOCTOR_NAME",
            "Department":   "DEPARTMENT",
            "Status":       "STATUS"
        }
        col = col_map.get(search_by, "PATIENT_NAME")
        conn = get_db()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Appointments WHERE {col} LIKE ?", (f"%{search_val}%",))
        results = cur.fetchall()
        conn.close()
    return render_template('search.html', results=results,
                           search_val=search_val, search_by=search_by)

# ---- Cancel Appointment ----
@app.route('/cancel/<int:appt_id>')
def cancel(appt_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT DOCTOR_ID FROM Appointments WHERE APPOINTMENT_ID=?", (appt_id,))
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE Appointments SET STATUS='Cancelled' WHERE APPOINTMENT_ID=?", (appt_id,))
        cur.execute("UPDATE Doctors SET CURRENT_PATIENTS=MAX(0,CURRENT_PATIENTS-1) WHERE DOCTOR_ID=?", (row['DOCTOR_ID'],))
        conn.commit()
    conn.close()
    flash("Appointment cancelled successfully!", "info")
    return redirect(url_for('appointments'))

# ---- Doctors Page ----
@app.route('/doctors')
def doctors():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Doctors ORDER BY DEPARTMENT")
    rows = cur.fetchall()
    conn.close()
    return render_template('doctors.html', doctors=rows)

if __name__ == '__main__':
    from create_db import create_database
    create_database()
    app.run(debug=True)
