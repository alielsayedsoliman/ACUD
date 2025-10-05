# app.py
from flask import Flask
from Controller.student import StudentController
from Controller.Mentor import MentorController
from Controller.Recruiter import RecruiterController
from Controller.AuthController import AuthController
from Controller.InternshipController import InternshipController
from Controller.EnrollmentController import EnrollmentController
from Route.course import course_bp
from Route.student import student_bp
from Route.mentorship_routes import mentorship_bp
from Route.recruiter import recruiter_bp
from Route.chat import chat_bp, socketio   # ✅ chat blueprint & socketio

# Create Flask app
app = Flask(__name__)

# ======================
# Students
# ======================
app.add_url_rule('/students', view_func=StudentController.get_students, methods=['GET'])
app.add_url_rule('/students/register', view_func=StudentController.register_student, methods=['POST'])

# ======================
# Mentors
# ======================
app.add_url_rule('/mentors', view_func=MentorController.get_mentors, methods=['GET'])
app.add_url_rule('/mentors/register', view_func=MentorController.register_mentor, methods=['POST'])

# ======================
# Internships
# ======================
app.add_url_rule('/internships', view_func=InternshipController.get_internships, methods=['GET'])
app.add_url_rule('/internships/create', view_func=InternshipController.create_internship, methods=['POST'])
app.add_url_rule('/internships/<int:internshipID>', view_func=InternshipController.update_internship, methods=['PUT'])

# ======================
# Enrollment
# ======================
app.add_url_rule('/courses/enroll', view_func=EnrollmentController.enroll_course, methods=['POST'])
app.add_url_rule('/internships/enroll', view_func=EnrollmentController.enroll_internship, methods=['POST'])
app.add_url_rule('/students/<student_id>/courses', view_func=EnrollmentController.get_student_courses, methods=['GET'])
app.add_url_rule('/students/<student_id>/internships', view_func=EnrollmentController.get_student_internships, methods=['GET'])

# ======================
# Blueprints
# ======================
app.register_blueprint(course_bp)
app.register_blueprint(student_bp)
app.register_blueprint(mentorship_bp, url_prefix="/mentorship")
app.register_blueprint(recruiter_bp)
app.register_blueprint(chat_bp)  # ✅ شغل الشات

# ======================
# Auth
# ======================
app.add_url_rule('/login', view_func=AuthController.login, methods=['POST'])

# ======================
# Run App with SocketIO
# ======================
if __name__ == '__main__':
    socketio.init_app(app, cors_allowed_origins="*")  # اربط socketio بالـ app
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
