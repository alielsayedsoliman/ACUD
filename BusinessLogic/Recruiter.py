from Model.recruiter import RecruiterModel

class RecruiterService:
    @staticmethod
    def fetch_all_recruiters(page=1, items_per_page=10):
        return RecruiterModel.get_all_recruiters(page, items_per_page)

    @staticmethod
    def register_recruiter(data):
        required = ("userID", "first_name", "middle_name", "last_name", "location", "password", "email")
        if not all(k in data for k in required):
            return {"error": "Missing required fields"}
        return RecruiterModel.insert_user_and_recruiter(data)
