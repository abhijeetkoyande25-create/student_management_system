# Flask Student Management Web App

This project is a university student management web application built with Python, Flask, and SQLite.

## Features

- Dashboard with student directory and quick statistics
- Student detail page with full personal, parent, fees, course, and previous college information
- Add and edit student records
- Course-based subject assignment
- Attendance, assignment count, and marks for each subject
- Project completion tracking
- Separate results page with all subject marks and SGPA
- SQLite database storage

## Project Structure

- `app.py` : Flask application and routes
- `templates/` : Jinja templates for pages
- `static/` : CSS and JavaScript assets
- `instance/student_management.db` : SQLite database created at runtime
- `requirements.txt` : Python dependencies

## How to Run

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
python app.py
```

5. Open the local URL shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

## Notes

- The SQLite database is created automatically on first run.
- Sample student records are seeded automatically the first time the app starts.
- Older demo files were replaced with this Flask web app structure.
