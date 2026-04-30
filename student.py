from dataclasses import asdict, dataclass


@dataclass
class Student:
    student_id: str
    full_name: str
    department: str
    year: int
    email: str
    phone: str
    gpa: float
    status: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(
            student_id=str(data["student_id"]).strip(),
            full_name=str(data["full_name"]).strip(),
            department=str(data["department"]).strip(),
            year=int(data["year"]),
            email=str(data["email"]).strip(),
            phone=str(data["phone"]).strip(),
            gpa=float(data["gpa"]),
            status=str(data["status"]).strip(),
        )
