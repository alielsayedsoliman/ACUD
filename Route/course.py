from flask import Blueprint, request, jsonify
from Controller.course import CourseController

course_bp = Blueprint("course_bp", __name__)

@course_bp.route("/courses", methods=["GET"])
def get_courses():
    page = request.args.get('page', default=1, type=int)
    items_per_page = request.args.get('items_per_page', default=10, type=int)

    if page < 1:
        return jsonify({"error": "Page number must be greater than 0"}), 400
    if items_per_page < 1:
        return jsonify({"error": "Items per page must be greater than 0"}), 400

    return CourseController.get_courses(page, items_per_page)

@course_bp.route("/courses/<course_id>", methods=["GET"])
def get_course(course_id):
    return CourseController.get_course(course_id)

@course_bp.route("/courses", methods=["POST"])
def create_course():
    return CourseController.create_course()

@course_bp.route("/courses/<course_id>", methods=["PUT"])
def update_course(course_id):
    return CourseController.update_course(course_id)

@course_bp.route("/courses/<course_id>", methods=["DELETE"])
def delete_course(course_id):
    return CourseController.delete_course(course_id)
