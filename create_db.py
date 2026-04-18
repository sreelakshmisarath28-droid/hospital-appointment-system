import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hospital.db')

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Doctors(
        DOCTOR_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DOCTOR_NAME text NOT NULL,
        DEPARTMENT text NOT NULL,
        QUALIFICATION text,
        EXPERIENCE text,
        AVAILABLE_DAYS text,
        MAX_PATIENTS integer DEFAULT 10,
        CURRENT_PATIENTS integer DEFAULT 0
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Appointments(
        APPOINTMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PATIENT_NAME text NOT NULL,
        AGE text,
        GENDER text,
        CONTACT text,
        EMAIL text,
        DEPARTMENT text,
        DOCTOR_ID integer,
        DOCTOR_NAME text,
        APPOINTMENT_DATE text,
        APPOINTMENT_TIME text,
        SYMPTOMS text,
        STATUS text DEFAULT 'Confirmed',
        BOOKED_ON text
    )""")

    cur.execute("SELECT COUNT(*) FROM Doctors")
    if cur.fetchone()[0] == 0:
        doctors = [
            ("Dr. Rahul Sharma",  "General",     "MBBS, MD",        "10 years", "Mon,Tue,Wed,Thu,Fri", 15, 0),
            ("Dr. Priya Nair",    "General",     "MBBS",            "5 years",  "Mon,Wed,Fri",         12, 0),
            ("Dr. Arun Kumar",    "Cardiology",  "MBBS, DM",        "12 years", "Mon,Tue,Thu",         10, 0),
            ("Dr. Meena Pillai",  "Cardiology",  "MBBS, MD, DM",    "8 years",  "Tue,Wed,Fri",         10, 0),
            ("Dr. Suresh Menon",  "Neurology",   "MBBS, DM Neuro",  "15 years", "Mon,Wed,Thu",         8,  0),
            ("Dr. Anitha George", "Neurology",   "MBBS, MD",        "7 years",  "Tue,Thu,Fri",         8,  0),
            ("Dr. Vijay Patel",   "Orthopaedic", "MBBS, MS Ortho",  "11 years", "Mon,Tue,Wed",         10, 0),
            ("Dr. Rekha Das",     "Orthopaedic", "MBBS, DNB",       "6 years",  "Wed,Thu,Fri",         10, 0),
            ("Dr. Kavitha Iyer",  "Paediatric",  "MBBS, MD Paed",   "9 years",  "Mon,Tue,Thu,Fri",     12, 0),
            ("Dr. Ravi Krishnan", "Paediatric",  "MBBS, DCH",       "4 years",  "Mon,Wed,Fri",         12, 0),
            ("Dr. Shalini Reddy", "Gynaecology", "MBBS, MS Gynae",  "13 years", "Tue,Wed,Thu",         10, 0),
            ("Dr. Lakshmi Bose",  "Gynaecology", "MBBS, DGO",       "7 years",  "Mon,Thu,Fri",         10, 0),
            ("Dr. Deepak Nair",   "Dermatology", "MBBS, MD Derm",   "9 years",  "Mon,Tue,Fri",         12, 0),
            ("Dr. Suma Varma",    "Dermatology", "MBBS, DVD",       "5 years",  "Wed,Thu,Fri",         12, 0),
        ]
        cur.executemany("INSERT INTO Doctors(DOCTOR_NAME,DEPARTMENT,QUALIFICATION,EXPERIENCE,AVAILABLE_DAYS,MAX_PATIENTS,CURRENT_PATIENTS) VALUES(?,?,?,?,?,?,?)", doctors)

    conn.commit()
    conn.close()
    print("Hospital database created successfully!")

if __name__ == "__main__":
    create_database()
