from flask import Blueprint, request, jsonify
from Controller.student import StudentController

student_bp = Blueprint("student_bp", __name__)


@student_bp.route("/students/register", methods=["POST"])
def register_student():
    return StudentController.register_student()

@student_bp.route("/students", methods=["GET"])
def get_students():
    page = request.args.get('page', default=1, type=int)
    items_per_page = request.args.get('items_per_page', default=10, type=int)

    if page < 1:
        return jsonify({"error": "Page number must be greater than 0"}), 400
    if items_per_page < 1:
        return jsonify({"error": "Items per page must be greater than 0"}), 400

    return StudentController.get_students(page, items_per_page)


@student_bp.route("/students/<user_id>", methods=["PUT"])
def update_student(user_id):
    return StudentController.update_student(user_id)
