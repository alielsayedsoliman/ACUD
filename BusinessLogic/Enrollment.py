# BusinessLogic/Enrollment.py (نكمل عليه)
from Model.enrollment import EnrollmentModel

class EnrollmentService:
    @staticmethod
    def enroll_course(data):
        if "userID" not in data or "coursesID" not in data:
            return {"error": "userID and coursesID required"}
        return EnrollmentModel.enroll_course(data["userID"], data["coursesID"])

    @staticmethod
    def enroll_internship(data):
        if "studentID" not in data or "internshipID" not in data:
            return {"error": "studentID and internshipID required"}
        return EnrollmentModel.enroll_internship(data["studentID"], data["internshipID"])

    @staticmethod
    def get_student_courses(student_id):
        return EnrollmentModel.get_student_courses(student_id)

    @staticmethod
    def get_student_internships(student_id):
        return EnrollmentModel.get_student_internships(student_id)
