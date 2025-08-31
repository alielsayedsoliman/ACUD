from flask import Blueprint
from Controller.student import StudentController

student_bp = Blueprint("student_bp", __name__)


@student_bp.route("/students/register", methods=["POST"])
def register_student():
    return StudentController.register_student()

@student_bp.route("/students", methods=["GET"])
def get_students():
    return StudentController.get_students()
