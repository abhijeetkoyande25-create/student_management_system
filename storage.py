import json
from pathlib import Path

from student import Student


class StudentStorage:
    def __init__(self, file_path: str = "data/students.json") -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_students(self) -> list[Student]:
        if not self.file_path.exists():
            students = self._seed_students()
            self.save_students(students)
            return students

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [Student.from_dict(item) for item in data]

    def save_students(self, students: list[Student]) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump([student.to_dict() for student in students], file, indent=2)

    def _seed_students(self) -> list[Student]:
        return [
            Student(
                student_id="UNI001",
                full_name="Aarav Sharma",
                department="Computer Science",
                year=2,
                email="aarav.sharma@university.edu",
                phone="9876543210",
                gpa=8.7,
                status="Active",
            ),
            Student(
                student_id="UNI002",
                full_name="Priya Patel",
                department="Electronics",
                year=3,
                email="priya.patel@university.edu",
                phone="9876501234",
                gpa=9.1,
                status="Active",
            ),
        ]
