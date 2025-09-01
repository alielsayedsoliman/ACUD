from flask import Flask
from Route.student import student_bp
from Route.course import course_bp

app = Flask(__name__)

# Register blueprints (routes)
app.register_blueprint(student_bp)
app.register_blueprint(course_bp)

if __name__ == "__main__":
    app.run(debug=True)
