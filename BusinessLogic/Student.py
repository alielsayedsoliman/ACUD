from Model.student import StudentModel

class StudentService:
    @staticmethod
    def fetch_all_students():
        students = StudentModel.get_all_students()
        # Example of extra business logic (filter, sort, etc.)
        return students
    
     
    @staticmethod
    def register_student(data):
        # Example business logic: could add validation here later
        if not all(key in data for key in ("userID", "first_name", "middle_name", "last_name", "location", "profile_pic", "personal_summary", "password", "email")):
            return {"error": "Missing required fields"}
        
        return StudentModel.insert_user_and_student(data)