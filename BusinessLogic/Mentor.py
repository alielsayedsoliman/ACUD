from Model.mentor import MentorModel

class MentorService:
    @staticmethod
    def fetch_all_mentors():
        return MentorModel.get_all_mentors()

    @staticmethod
    def register_mentor(data):
        required = ("userID", "first_name", "middle_name", "last_name", "location", "password", "email", "professional_background", "expertise")
        if not all(k in data for k in required):
            return {"error": "Missing required fields"}
        return MentorModel.insert_user_and_mentor(data)
