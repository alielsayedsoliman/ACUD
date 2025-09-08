# BusinessLogic/Internship.py
from Model.internship import InternshipModel

class InternshipService:
    @staticmethod
    def fetch_all_internships():
        return InternshipModel.get_all_internships()

    @staticmethod
    def create_internship(data):
        required = ("recruiterID", "title")
        if not all(k in data for k in required):
            return {"error": "Missing required fields"}
        return InternshipModel.create_internship(data)

    @staticmethod
    def update_internship(internshipID, data):
        # Validate data
        if not data:
            return {"error": "No update data provided"}
            
        allowed_fields = ["title", "description", "location", "start_date", "end_date"]
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return {"error": "No valid fields to update"}

        return InternshipModel.update_internship(internshipID, update_data)
