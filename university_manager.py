from student import Student
from storage import StudentStorage


class UniversityStudentManager:
    def __init__(self) -> None:
        self.storage = StudentStorage()
        self.students = self.storage.load_students()

    def add_student(self, student: Student) -> bool:
        if self.find_student_by_id(student.student_id):
            return False

        self.students.append(student)
        self.storage.save_students(self.students)
        return True

    def list_students(self) -> list[Student]:
        return sorted(self.students, key=lambda student: student.student_id)

    def find_student_by_id(self, student_id: str) -> Student | None:
        for student in self.students:
            if student.student_id.lower() == student_id.lower():
                return student
        return None

    def search_students(self, keyword: str) -> list[Student]:
        query = keyword.strip().lower()
        return [
            student
            for student in self.students
            if query in student.student_id.lower()
            or query in student.full_name.lower()
            or query in student.department.lower()
            or query in student.email.lower()
            or query in student.status.lower()
        ]

    def update_student(self, student_id: str, updated_student: Student) -> bool:
        for index, student in enumerate(self.students):
            if student.student_id.lower() == student_id.lower():
                if (
                    updated_student.student_id.lower() != student_id.lower()
                    and self.find_student_by_id(updated_student.student_id)
                ):
                    return False

                self.students[index] = updated_student
                self.storage.save_students(self.students)
                return True
        return False

    def delete_student(self, student_id: str) -> bool:
        for index, student in enumerate(self.students):
            if student.student_id.lower() == student_id.lower():
                del self.students[index]
                self.storage.save_students(self.students)
                return True
        return False

    def get_summary(self) -> dict:
        total_students = len(self.students)
        if total_students == 0:
            return {
                "total_students": 0,
                "average_gpa": 0.0,
                "active_students": 0,
                "inactive_students": 0,
            }

        average_gpa = sum(student.gpa for student in self.students) / total_students
        active_students = sum(student.status.lower() == "active" for student in self.students)

        return {
            "total_students": total_students,
            "average_gpa": round(average_gpa, 2),
            "active_students": active_students,
            "inactive_students": total_students - active_students,
        }
