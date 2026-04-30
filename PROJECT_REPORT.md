# Student Management System Project Report

## 1. Project Title

**Student Management System using Python, Flask, and SQLite**

## 2. Introduction

The Student Management System is a web-based application developed to manage university student records in a structured and efficient way. The main purpose of this project is to reduce manual paperwork and provide a centralized system for storing, updating, and viewing student-related information.

This project allows an administrator to manage complete student profiles, including:

- Student personal details
- Parent details
- Enrollment year
- Selected course
- Previous college information
- Fee payment details
- Subject assignment
- Attendance
- Assignment count
- Marks and SGPA
- Project completion status

The application is developed using **Python** as the programming language, **Flask** as the web framework, and **SQLite** as the database for storing records.

## 3. Problem Statement

In many colleges and universities, student information is often stored in spreadsheets, notebooks, or separate files. This creates several problems:

- Data duplication
- Difficulty in updating records
- Lack of a proper result tracking system
- No centralized fee and attendance management
- Time-consuming manual operations

To solve these issues, this Student Management System was created as a simple and organized web application.

## 4. Objectives

The main objectives of this project are:

- To create a centralized system for student data management
- To store complete student details in a database
- To track fees paid and pending amounts
- To assign subjects based on the selected course
- To maintain attendance and assignment counts for each subject
- To calculate and display student SGPA
- To provide a separate result page for academic performance
- To make student information easy to search, update, and delete

## 5. Scope of the Project

The scope of this project includes university-level student management for administrative use. It covers:

- Student registration
- Student profile management
- Academic record management
- Result generation
- Fee management
- Parent and previous education details

This project is suitable for:

- Colleges
- Universities
- Training institutes
- Academic administration demo projects

## 6. Technology Stack

The following technologies are used in this project:

- **Python**: Core programming language
- **Flask**: Backend web framework
- **SQLite**: Lightweight relational database
- **HTML**: Page structure
- **CSS**: User interface styling
- **JavaScript**: Dynamic subject rendering in forms
- **Jinja2**: Template rendering engine used by Flask

## 7. System Architecture

The project follows a simple web application architecture:

1. The user opens the application in a web browser.
2. Flask handles the request from the browser.
3. Flask processes business logic and communicates with SQLite.
4. Data is fetched, stored, updated, or deleted from the database.
5. Flask renders HTML templates and sends the response back to the browser.

### Architecture Components

- **Frontend**
  - HTML templates in the `templates` folder
  - CSS and JavaScript in the `static` folder

- **Backend**
  - `app.py` contains routes, form processing, validation, and database handling

- **Database**
  - SQLite database file stored in the `instance` folder

## 8. Project Modules

The project is divided into the following modules:

### 8.1 Dashboard Module

This module displays:

- Total number of students
- Number of students with pending fees
- Average SGPA
- Number of completed projects
- Student directory
- Quick student detail summary

### 8.2 Student Registration Module

This module is used to add new student records. It includes:

- Student ID
- Full name
- Enrollment year
- Current year/semester
- Course
- Status
- Email
- Phone number
- Address
- Parent name
- Parent phone number
- Previous college name
- Previous course
- Previous marks
- Total fees
- Fees paid
- Project completion status

### 8.3 Subject Management Module

Subjects are assigned automatically based on the selected course. For each subject, the system stores:

- Subject name
- Attendance percentage
- Assignment count
- Marks

### 8.4 Student Detail Module

This module provides a full profile view of a selected student. It shows:

- Basic information
- Contact details
- Parent details
- Previous college details
- Fee information
- Project status
- Academic summary
- Subject-wise progress

### 8.5 Result Module

This module provides a separate result page that displays:

- Course
- Current year/semester
- Subject-wise marks
- Attendance
- Assignment count
- Pass or needs improvement status
- SGPA

### 8.6 Update and Delete Module

This module allows the administrator to:

- Edit an existing student record
- Delete an existing student record

## 9. Database Design

The project uses SQLite with two main tables.

### 9.1 Students Table

This table stores the main student profile information.

Important fields:

- `id`
- `student_id`
- `full_name`
- `enrollment_year`
- `current_year`
- `course`
- `status`
- `student_email`
- `student_phone`
- `student_address`
- `parent_name`
- `parent_phone`
- `previous_college_name`
- `previous_course`
- `previous_marks`
- `total_fees`
- `fees_paid`
- `project_completed`

### 9.2 Student Subjects Table

This table stores subject-related academic data for each student.

Important fields:

- `id`
- `student_id`
- `subject_name`
- `attendance`
- `assignments_count`
- `marks`

### Relationship

- One student can have multiple subjects.
- The relationship between `students` and `student_subjects` is **one-to-many**.

## 10. Features of the System

The main features of this Student Management System are:

- Web-based interface
- Clean and modern dashboard
- Course-based subject assignment
- Full student profile management
- Parent and previous college information storage
- Fees paid and pending tracking
- Attendance and assignment tracking
- Subject-wise marks storage
- SGPA calculation
- Result sheet page
- Search functionality
- Edit and delete records
- SQLite-based persistent data storage
- Automatic sample data seeding on first run

## 11. Functional Workflow

The working flow of the project is as follows:

1. The administrator opens the application.
2. The dashboard displays student records and summary statistics.
3. The administrator can add a new student from the Add Student page.
4. Based on the selected course, the subject list is generated automatically.
5. The administrator enters attendance, assignments, and marks for each subject.
6. The data is validated and saved into the SQLite database.
7. The student detail page shows complete information.
8. The result page displays subject marks and SGPA.
9. The administrator can edit or delete records whenever required.

## 12. Input Validation

The system performs validation for important fields, such as:

- Unique student ID
- Valid enrollment year
- Previous marks range from 0 to 100
- Attendance range from 0 to 100
- Marks range from 0 to 100
- Fees paid should not exceed total fees
- Required fields must not be empty

This validation improves data accuracy and prevents incorrect records from being stored.

## 13. SGPA Calculation Logic

The project calculates SGPA based on subject marks using grade points.

### Grade Point Mapping

- 90 and above = 10
- 80 to 89 = 9
- 70 to 79 = 8
- 60 to 69 = 7
- 50 to 59 = 6
- 40 to 49 = 5
- Below 40 = 0

### SGPA Formula

**SGPA = Total Grade Points / Number of Subjects**

This gives a simple academic performance indicator for each student.

## 14. User Interface Pages

The application contains the following pages:

### Dashboard Page

- Summary cards
- Student directory
- Quick student detail panel

### Add/Edit Student Page

- Complete form for entering or updating student records
- Dynamic subject fields based on selected course

### Student Detail Page

- Full student profile
- Fee summary
- Previous education summary
- Subject progress cards

### Results Page

- Student selection panel
- Subject-wise marks table
- SGPA display
- Attendance and assignment summary

## 15. File Structure

Main project files and folders:

- `app.py`
- `requirements.txt`
- `README.md`
- `templates/`
- `static/`
- `instance/`

### Templates Folder

- `base.html`
- `dashboard.html`
- `student_form.html`
- `student_detail.html`
- `results.html`

### Static Folder

- `style.css`
- `app.js`

## 16. Advantages of the Project

- Easy to use
- Better than manual student record keeping
- Data stored in a structured database
- Supports quick search and updates
- Helps monitor academic and fee status together
- Useful for mini project or academic submission
- Can be extended easily into a larger ERP-style system

## 17. Limitations

Current limitations of the project include:

- No student login or admin authentication
- No role-based access
- No PDF report generation
- No online payment integration
- No cloud deployment by default
- No advanced analytics or charts

These limitations can be addressed in future versions.

## 18. Future Enhancements

The project can be improved further by adding:

- Admin login system
- Student login panel
- Faculty login panel
- PDF report generation
- Excel export
- Attendance charts and analytics
- Fee receipt generation
- Email or SMS notifications
- Cloud hosting
- Multi-user support
- Semester-wise result history
- File upload for student documents

## 19. Testing Approach

The project should be tested in the following areas:

- Student record creation
- Student edit and delete operations
- Database insertion and retrieval
- Search functionality
- Subject rendering based on course
- SGPA calculation correctness
- Result page accuracy
- Fee calculation correctness
- Form validation messages

## 20. Conclusion

The Student Management System developed using Python, Flask, and SQLite is a practical web application for handling student records efficiently. It combines administrative, academic, and fee-related functions into a single platform. The project demonstrates how a lightweight web framework and database can be used to build a useful real-world academic management solution.

This project is suitable for academic submission, portfolio use, and further enhancement into a complete college management system.

## 21. How to Run the Project

1. Install Python on the system
2. Open terminal in the project folder
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the Flask application:

```bash
python app.py
```

5. Open the browser and visit:

```text
http://127.0.0.1:5000
```

## 22. Summary

This project successfully implements:

- Student profile management
- Parent detail management
- Course and subject management
- Attendance and assignment tracking
- Fees tracking
- Project completion tracking
- Subject-wise result display
- SGPA calculation
- Database-based storage with Flask and SQLite
