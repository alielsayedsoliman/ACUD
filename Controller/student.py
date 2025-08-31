from BusinessLogic.Student import StudentService
from flask import request, jsonify

class StudentController:
    @staticmethod
    def get_students():
        students = StudentService.fetch_all_students()
        return jsonify({"students": students})
    
    def register_student():
        data = request.get_json()
        result = StudentService.register_student(data)
        return jsonify(result)