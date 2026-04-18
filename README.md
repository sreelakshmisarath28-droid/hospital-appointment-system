# 🏥 Hospital Appointment System with Smart Scheduling

A web-based hospital appointment management system built with **Python, Flask, SQLite and HTML/CSS**. Features automatic doctor assignment based on availability — no manual doctor selection needed.

---

## Features

- Book patient appointments online (web browser)
- Smart scheduling — doctor auto-assigned based on department & availability
- View all appointments in a table
- Search by Patient Name, Doctor, Department or Status
- Cancel appointments
- View all doctors and their availability status
- Green & White medical theme
- 14 pre-loaded doctors across 7 departments

---

## Project Structure

```
hospital_appointment/
│
├── app.py               # Main Flask application (run this)
├── create_db.py         # Creates SQLite database with sample doctors
├── requirements.txt     # Python dependencies
├── hospital.db          # Auto-created on first run
│
├── templates/
│   ├── base.html        # Base layout
│   ├── index.html       # Home page
│   ├── book.html        # Book appointment page
│   ├── appointments.html # View all appointments
│   ├── search.html      # Search appointments
│   └── doctors.html     # View all doctors
│
└── static/
    └── css/
        └── style.css    # Green & White medical theme
```

---

## How to Run

### Step 1 — Install Flask
```bash
pip install -r requirements.txt
```

### Step 2 — Run the app
```bash
python app.py
```

### Step 3 — Open in browser
```
http://127.0.0.1:5000
```

---

## Departments Available

- General
- Cardiology
- Neurology
- Orthopaedic
- Paediatric
- Gynaecology
- Dermatology

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web framework |
| SQLite | Database |
| HTML/CSS | Frontend web pages |
| Jinja2 | Template engine (comes with Flask) |

---

## CV Description

> Developed a web-based Hospital Appointment Management System using Python and Flask with SQLite database. Implemented smart scheduling logic to automatically assign the most available doctor based on department and current patient load. Features include online appointment booking, multi-field search, appointment cancellation, and a doctor availability dashboard.

## Duration
July 2025 – February 2026 | Solo Developer
