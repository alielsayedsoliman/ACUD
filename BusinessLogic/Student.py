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
        if not all(key in data for key in ("User_ID", "name", "phone_number", "email", "location", "password")):
            return {"error": "Missing required fields"}
        
        return StudentModel.insert_user_and_student(data)