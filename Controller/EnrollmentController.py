# Controller/EnrollmentController.py (نكمل عليه)
from BusinessLogic.Enrollment import EnrollmentService
from flask import request, jsonify

class EnrollmentController:
    @staticmethod
    def enroll_course():
        data = request.get_json()
        result = EnrollmentService.enroll_course(data)
        return jsonify(result)

    @staticmethod
    def enroll_internship():
        data = request.get_json()
        result = EnrollmentService.enroll_internship(data)
        return jsonify(result)

    @staticmethod
    def get_student_courses(student_id):
        courses = EnrollmentService.get_student_courses(student_id)
        return jsonify({"courses": courses})

    @staticmethod
    def get_student_internships(student_id):
        internships = EnrollmentService.get_student_internships(student_id)
        return jsonify({"internships": internships})
