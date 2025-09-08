from BusinessLogic.Student import StudentService
from flask import request, jsonify

class StudentController:
    @staticmethod
    def get_students(page=1, items_per_page=10):
        result = StudentService.fetch_all_students(page, items_per_page)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result)
    
    def register_student():
        data = request.get_json()
        result = StudentService.register_student(data)
        return jsonify(result)
    


    @staticmethod
    def update_student(user_id):
        data = request.get_json()
        result = StudentService.update_student(user_id, data)

        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 200