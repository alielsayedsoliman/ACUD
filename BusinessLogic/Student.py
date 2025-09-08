from Model.student import StudentModel

class StudentService:
    @staticmethod
    def fetch_all_students(page=1, items_per_page=10):
        result = StudentModel.get_all_students(page, items_per_page)
        # Example of extra business logic (filter, sort, etc.)
        return result
    
     
    @staticmethod
    def register_student(data):
        # Example business logic: could add validation here later
        if not all(key in data for key in ("userID", "first_name", "middle_name", "last_name", "location", "profile_pic", "personal_summary", "email" , "password")):
            return {"error": "Missing required fields"}
        
        return StudentModel.insert_user_and_student(data)
    
    @staticmethod
    def update_student(user_id, data):
        profile_pic = data.get("profile_pic")
        personal_summary = data.get("personal_summary")

        if not profile_pic and not personal_summary:
            return {"error": "No fields to update"}

        return StudentModel.update_profile(user_id, profile_pic, personal_summary)