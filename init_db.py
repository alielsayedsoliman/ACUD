from app import app, db
from Model.mentorship import Student, Mentor, Mentorship

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created.")

if __name__ == '__main__':
    init_db()
