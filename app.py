from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, flash, g, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "instance" / "student_management.db"

COURSE_SUBJECTS = {
    "BCA": [
        "Programming in C",
        "Database Systems",
        "Web Technology",
        "Mathematics",
        "Communication Skills",
    ],
    "BBA": [
        "Principles of Management",
        "Business Economics",
        "Financial Accounting",
        "Marketing",
        "Business Communication",
    ],
    "BCom": [
        "Financial Accounting",
        "Corporate Law",
        "Business Statistics",
        "Taxation",
        "Economics",
    ],
    "BSc IT": [
        "Operating Systems",
        "Networking",
        "Python Programming",
        "Data Structures",
        "Cloud Fundamentals",
    ],
    "MBA": [
        "Strategic Management",
        "Finance",
        "Human Resources",
        "Operations",
        "Business Analytics",
    ],
}


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"
app.config["DATABASE"] = DATABASE_PATH
app.config["DB_READY"] = False


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_: BaseException | None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            enrollment_year INTEGER NOT NULL,
            current_year TEXT NOT NULL,
            course TEXT NOT NULL,
            status TEXT NOT NULL,
            student_email TEXT NOT NULL,
            student_phone TEXT NOT NULL,
            student_address TEXT NOT NULL,
            parent_name TEXT NOT NULL,
            parent_phone TEXT NOT NULL,
            previous_college_name TEXT NOT NULL,
            previous_course TEXT NOT NULL,
            previous_marks REAL NOT NULL,
            total_fees REAL NOT NULL,
            fees_paid REAL NOT NULL,
            project_completed TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS student_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_name TEXT NOT NULL,
            attendance REAL NOT NULL,
            assignments_count INTEGER NOT NULL,
            marks REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
        );
        """
    )
    db.commit()
    seed_data(db)
    app.config["DB_READY"] = True


@app.before_request
def ensure_db_ready() -> None:
    if not app.config["DB_READY"]:
        init_db()


def seed_data(db: sqlite3.Connection) -> None:
    existing = db.execute("SELECT COUNT(*) AS total FROM students").fetchone()["total"]
    if existing:
        return

    seeded_students = [
        {
            "student_id": "UNI101",
            "full_name": "Aarav Sharma",
            "enrollment_year": 2024,
            "current_year": "Year 2 / Sem 4",
            "course": "BCA",
            "status": "Active",
            "student_email": "aarav.sharma@university.edu",
            "student_phone": "9876543210",
            "student_address": "Pune, Maharashtra",
            "parent_name": "Rakesh Sharma",
            "parent_phone": "9898989898",
            "previous_college_name": "Sunrise Junior College",
            "previous_course": "Science",
            "previous_marks": 84.0,
            "total_fees": 120000.0,
            "fees_paid": 90000.0,
            "project_completed": "No",
            "subjects": [
                {"subject_name": "Programming in C", "attendance": 88, "assignments_count": 5, "marks": 82},
                {"subject_name": "Database Systems", "attendance": 91, "assignments_count": 4, "marks": 86},
                {"subject_name": "Web Technology", "attendance": 85, "assignments_count": 6, "marks": 79},
                {"subject_name": "Mathematics", "attendance": 80, "assignments_count": 5, "marks": 74},
                {"subject_name": "Communication Skills", "attendance": 93, "assignments_count": 3, "marks": 88},
            ],
        },
        {
            "student_id": "UNI102",
            "full_name": "Priya Patel",
            "enrollment_year": 2023,
            "current_year": "Year 3 / Sem 6",
            "course": "BBA",
            "status": "Active",
            "student_email": "priya.patel@university.edu",
            "student_phone": "9765432101",
            "student_address": "Ahmedabad, Gujarat",
            "parent_name": "Meena Patel",
            "parent_phone": "9777777777",
            "previous_college_name": "City Commerce College",
            "previous_course": "Commerce",
            "previous_marks": 89.0,
            "total_fees": 135000.0,
            "fees_paid": 135000.0,
            "project_completed": "Yes",
            "subjects": [
                {"subject_name": "Principles of Management", "attendance": 94, "assignments_count": 7, "marks": 90},
                {"subject_name": "Business Economics", "attendance": 90, "assignments_count": 5, "marks": 84},
                {"subject_name": "Financial Accounting", "attendance": 92, "assignments_count": 6, "marks": 88},
                {"subject_name": "Marketing", "attendance": 89, "assignments_count": 5, "marks": 91},
                {"subject_name": "Business Communication", "attendance": 95, "assignments_count": 4, "marks": 87},
            ],
        },
    ]

    for student in seeded_students:
        subjects = student.pop("subjects")
        cursor = db.execute(
            """
            INSERT INTO students (
                student_id, full_name, enrollment_year, current_year, course, status,
                student_email, student_phone, student_address, parent_name, parent_phone,
                previous_college_name, previous_course, previous_marks, total_fees, fees_paid,
                project_completed
            ) VALUES (
                :student_id, :full_name, :enrollment_year, :current_year, :course, :status,
                :student_email, :student_phone, :student_address, :parent_name, :parent_phone,
                :previous_college_name, :previous_course, :previous_marks, :total_fees, :fees_paid,
                :project_completed
            )
            """,
            student,
        )
        row_id = cursor.lastrowid
        for subject in subjects:
            db.execute(
                """
                INSERT INTO student_subjects (student_id, subject_name, attendance, assignments_count, marks)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    row_id,
                    subject["subject_name"],
                    subject["attendance"],
                    subject["assignments_count"],
                    subject["marks"],
                ),
            )
    db.commit()


def calculate_grade_point(marks: float) -> int:
    if marks >= 90:
        return 10
    if marks >= 80:
        return 9
    if marks >= 70:
        return 8
    if marks >= 60:
        return 7
    if marks >= 50:
        return 6
    if marks >= 40:
        return 5
    return 0


def calculate_sgpa(subjects: list[dict[str, Any]]) -> float:
    if not subjects:
        return 0.0
    total = sum(calculate_grade_point(float(subject["marks"])) for subject in subjects)
    return round(total / len(subjects), 2)


def average_attendance(subjects: list[dict[str, Any]]) -> float:
    if not subjects:
        return 0.0
    total = sum(float(subject["attendance"]) for subject in subjects)
    return round(total / len(subjects), 1)


def get_subjects_for_student(student_row_id: int) -> list[dict[str, Any]]:
    db = get_db()
    rows = db.execute(
        """
        SELECT subject_name, attendance, assignments_count, marks
        FROM student_subjects
        WHERE student_id = ?
        ORDER BY id
        """,
        (student_row_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def build_student_payload(row: sqlite3.Row) -> dict[str, Any]:
    student = dict(row)
    subjects = get_subjects_for_student(student["id"])
    student["subjects"] = subjects
    student["fees_pending"] = round(float(student["total_fees"]) - float(student["fees_paid"]), 2)
    student["sgpa"] = calculate_sgpa(subjects)
    student["average_attendance"] = average_attendance(subjects)
    student["total_assignments"] = sum(int(subject["assignments_count"]) for subject in subjects)
    return student


def get_student_or_404(student_row_id: int) -> dict[str, Any] | None:
    db = get_db()
    row = db.execute("SELECT * FROM students WHERE id = ?", (student_row_id,)).fetchone()
    return build_student_payload(row) if row else None


def get_all_students(query: str = "") -> list[dict[str, Any]]:
    db = get_db()
    base_sql = "SELECT * FROM students"
    params: tuple[Any, ...] = ()
    if query:
        like = f"%{query.strip().lower()}%"
        base_sql += """
            WHERE lower(student_id) LIKE ?
            OR lower(full_name) LIKE ?
            OR lower(course) LIKE ?
            OR lower(student_phone) LIKE ?
            OR lower(parent_name) LIKE ?
            OR lower(parent_phone) LIKE ?
        """
        params = (like, like, like, like, like, like)
    rows = db.execute(f"{base_sql} ORDER BY full_name ASC", params).fetchall()
    return [build_student_payload(row) for row in rows]


def get_stats(students: list[dict[str, Any]]) -> dict[str, Any]:
    total_students = len(students)
    if total_students == 0:
        return {
            "total_students": 0,
            "fees_pending_count": 0,
            "average_sgpa": 0.0,
            "project_completed_count": 0,
            "top_performer": None,
        }

    return {
        "total_students": total_students,
        "fees_pending_count": sum(1 for student in students if student["fees_pending"] > 0),
        "average_sgpa": round(sum(student["sgpa"] for student in students) / total_students, 2),
        "project_completed_count": sum(
            1 for student in students if student["project_completed"] == "Yes"
        ),
        "top_performer": max(students, key=lambda student: student["sgpa"]),
    }


def blank_form_data(course: str = "BCA") -> dict[str, Any]:
    return {
        "student_id": "",
        "full_name": "",
        "enrollment_year": "",
        "current_year": "",
        "course": course,
        "status": "Active",
        "student_email": "",
        "student_phone": "",
        "student_address": "",
        "parent_name": "",
        "parent_phone": "",
        "previous_college_name": "",
        "previous_course": "",
        "previous_marks": "",
        "total_fees": "",
        "fees_paid": "",
        "project_completed": "No",
        "subjects": [
            {
                "subject_name": subject,
                "attendance": 0,
                "assignments_count": 0,
                "marks": 0,
            }
            for subject in COURSE_SUBJECTS[course]
        ],
    }


def parse_student_form(form_data: Any, student_row_id: int | None = None) -> tuple[dict[str, Any] | None, str | None]:
    course = form_data.get("course", "BCA")
    try:
        enrollment_year = int(form_data.get("enrollment_year", "").strip())
        previous_marks = float(form_data.get("previous_marks", "").strip())
        total_fees = float(form_data.get("total_fees", "").strip())
        fees_paid = float(form_data.get("fees_paid", "").strip())
    except ValueError:
        return None, "Enter valid numeric values for year, marks, and fees."

    student = {
        "student_id": form_data.get("student_id", "").strip(),
        "full_name": form_data.get("full_name", "").strip(),
        "enrollment_year": enrollment_year,
        "current_year": form_data.get("current_year", "").strip(),
        "course": course,
        "status": form_data.get("status", "Active").strip(),
        "student_email": form_data.get("student_email", "").strip(),
        "student_phone": form_data.get("student_phone", "").strip(),
        "student_address": form_data.get("student_address", "").strip(),
        "parent_name": form_data.get("parent_name", "").strip(),
        "parent_phone": form_data.get("parent_phone", "").strip(),
        "previous_college_name": form_data.get("previous_college_name", "").strip(),
        "previous_course": form_data.get("previous_course", "").strip(),
        "previous_marks": previous_marks,
        "total_fees": total_fees,
        "fees_paid": fees_paid,
        "project_completed": form_data.get("project_completed", "No").strip(),
    }

    required_keys = [
        "student_id",
        "full_name",
        "current_year",
        "student_email",
        "student_phone",
        "student_address",
        "parent_name",
        "parent_phone",
        "previous_college_name",
        "previous_course",
    ]
    if any(not student[key] for key in required_keys):
        return None, "Fill in all required fields before saving."

    if not 2000 <= student["enrollment_year"] <= 2100:
        return None, "Enrollment year must be between 2000 and 2100."
    if not 0 <= student["previous_marks"] <= 100:
        return None, "Previous marks must be between 0 and 100."
    if student["fees_paid"] > student["total_fees"]:
        return None, "Fees paid cannot be greater than total fees."

    subjects: list[dict[str, Any]] = []
    for index, subject_name in enumerate(COURSE_SUBJECTS.get(course, [])):
        try:
            attendance = float(form_data.get(f"attendance_{index}", "0").strip() or 0)
            assignments_count = int(form_data.get(f"assignments_{index}", "0").strip() or 0)
            marks = float(form_data.get(f"marks_{index}", "0").strip() or 0)
        except ValueError:
            return None, "Subject attendance, assignments, and marks must be numeric."

        if not 0 <= attendance <= 100:
            return None, f"Attendance for {subject_name} must be between 0 and 100."
        if assignments_count < 0:
            return None, f"Assignments for {subject_name} cannot be negative."
        if not 0 <= marks <= 100:
            return None, f"Marks for {subject_name} must be between 0 and 100."

        subjects.append(
            {
                "subject_name": subject_name,
                "attendance": attendance,
                "assignments_count": assignments_count,
                "marks": marks,
            }
        )

    student["subjects"] = subjects

    db = get_db()
    existing = db.execute(
        "SELECT id FROM students WHERE lower(student_id) = lower(?)",
        (student["student_id"],),
    ).fetchone()
    if existing and existing["id"] != student_row_id:
        return None, "Student ID must be unique."

    return student, None


def save_student(student: dict[str, Any], student_row_id: int | None = None) -> int:
    db = get_db()
    payload = {
        key: value
        for key, value in student.items()
        if key != "subjects"
    }

    if student_row_id is None:
        cursor = db.execute(
            """
            INSERT INTO students (
                student_id, full_name, enrollment_year, current_year, course, status,
                student_email, student_phone, student_address, parent_name, parent_phone,
                previous_college_name, previous_course, previous_marks, total_fees, fees_paid,
                project_completed
            ) VALUES (
                :student_id, :full_name, :enrollment_year, :current_year, :course, :status,
                :student_email, :student_phone, :student_address, :parent_name, :parent_phone,
                :previous_college_name, :previous_course, :previous_marks, :total_fees, :fees_paid,
                :project_completed
            )
            """,
            payload,
        )
        student_row_id = cursor.lastrowid
    else:
        payload["id"] = student_row_id
        db.execute(
            """
            UPDATE students
            SET student_id = :student_id,
                full_name = :full_name,
                enrollment_year = :enrollment_year,
                current_year = :current_year,
                course = :course,
                status = :status,
                student_email = :student_email,
                student_phone = :student_phone,
                student_address = :student_address,
                parent_name = :parent_name,
                parent_phone = :parent_phone,
                previous_college_name = :previous_college_name,
                previous_course = :previous_course,
                previous_marks = :previous_marks,
                total_fees = :total_fees,
                fees_paid = :fees_paid,
                project_completed = :project_completed
            WHERE id = :id
            """,
            payload,
        )
        db.execute("DELETE FROM student_subjects WHERE student_id = ?", (student_row_id,))

    for subject in student["subjects"]:
        db.execute(
            """
            INSERT INTO student_subjects (student_id, subject_name, attendance, assignments_count, marks)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student_row_id,
                subject["subject_name"],
                subject["attendance"],
                subject["assignments_count"],
                subject["marks"],
            ),
        )
    db.commit()
    return student_row_id


@app.context_processor
def inject_globals() -> dict[str, Any]:
    return {"course_subjects_json": json.dumps(COURSE_SUBJECTS), "course_subjects": COURSE_SUBJECTS}


@app.route("/")
def dashboard() -> str:
    query = request.args.get("q", "").strip()
    students = get_all_students(query)
    selected_id = request.args.get("student_id", type=int)
    selected_student = None
    if selected_id is not None:
        selected_student = next((student for student in students if student["id"] == selected_id), None)
    if selected_student is None and students:
        selected_student = students[0]
    return render_template(
        "dashboard.html",
        students=students,
        selected_student=selected_student,
        stats=get_stats(students),
        query=query,
    )


@app.route("/students")
def students_redirect() -> Any:
    return redirect(url_for("dashboard"))


@app.route("/students/new", methods=["GET", "POST"])
def create_student() -> str | Any:
    selected_course = request.values.get("course", "BCA")
    form_data = blank_form_data(selected_course)
    if request.method == "POST":
        parsed_student, error = parse_student_form(request.form)
        if error:
            flash(error, "error")
            form_data = dict(request.form)
            form_data["subjects"] = build_subjects_from_form(request.form, selected_course)
        else:
            student_row_id = save_student(parsed_student)
            flash("Student record created successfully.", "success")
            return redirect(url_for("student_detail", student_id=student_row_id))
    return render_template("student_form.html", form_data=form_data, form_mode="create", student=None)


@app.route("/students/<int:student_id>")
def student_detail(student_id: int) -> str | Any:
    student = get_student_or_404(student_id)
    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("dashboard"))
    return render_template("student_detail.html", student=student)


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id: int) -> str | Any:
    existing_student = get_student_or_404(student_id)
    if existing_student is None:
        flash("Student not found.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        parsed_student, error = parse_student_form(request.form, student_id)
        if error:
            flash(error, "error")
            form_data = dict(request.form)
            form_data["subjects"] = build_subjects_from_form(request.form, request.form.get("course", existing_student["course"]))
            return render_template(
                "student_form.html",
                form_data=form_data,
                form_mode="edit",
                student=existing_student,
            )

        save_student(parsed_student, student_id)
        flash("Student record updated successfully.", "success")
        return redirect(url_for("student_detail", student_id=student_id))

    return render_template(
        "student_form.html",
        form_data=existing_student,
        form_mode="edit",
        student=existing_student,
    )


@app.route("/students/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id: int) -> Any:
    db = get_db()
    db.execute("DELETE FROM student_subjects WHERE student_id = ?", (student_id,))
    db.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.commit()
    flash("Student record deleted successfully.", "success")
    return redirect(url_for("dashboard"))


@app.route("/results")
def results_overview() -> str:
    query = request.args.get("q", "").strip()
    students = get_all_students(query)
    selected_id = request.args.get("student_id", type=int)
    selected_student = None
    if selected_id is not None:
        selected_student = next((student for student in students if student["id"] == selected_id), None)
    if selected_student is None and students:
        selected_student = students[0]
    return render_template("results.html", students=students, selected_student=selected_student, query=query)


def build_subjects_from_form(form_data: Any, course: str) -> list[dict[str, Any]]:
    subjects = []
    for index, subject_name in enumerate(COURSE_SUBJECTS.get(course, [])):
        subjects.append(
            {
                "subject_name": subject_name,
                "attendance": form_data.get(f"attendance_{index}", 0),
                "assignments_count": form_data.get(f"assignments_{index}", 0),
                "marks": form_data.get(f"marks_{index}", 0),
            }
        )
    return subjects


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
