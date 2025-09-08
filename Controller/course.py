from BusinessLogic.Course import CourseService
from flask import request, jsonify

class CourseController:
    @staticmethod
    def get_courses(page=1, items_per_page=10):
        result = CourseService.fetch_all_courses(page, items_per_page)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result)
    
    @staticmethod
    def get_course(course_id):
        result = CourseService.get_course(course_id)
        if "error" in result:
            return jsonify(result), 404
        return jsonify({"course": result})
    
    @staticmethod
    def create_course():
        data = request.get_json()
        result = CourseService.create_course(data)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 201
    
    @staticmethod
    def update_course(course_id):
        data = request.get_json()
        result = CourseService.update_course(course_id, data)
        if "error" in result:
            return jsonify(result), 404 if result["error"] == "Course not found" else 400
        return jsonify(result)
    
    @staticmethod
    def delete_course(course_id):
        result = CourseService.delete_course(course_id)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 204
