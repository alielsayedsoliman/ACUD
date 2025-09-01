from flask import Blueprint
from Controller.course import CourseController

course_bp = Blueprint("course_bp", __name__)

@course_bp.route("/courses", methods=["GET"])
def get_courses():
    return CourseController.get_courses()

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
