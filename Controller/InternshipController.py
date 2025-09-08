# Controller/InternshipController.py
from BusinessLogic.Internship import InternshipService
from flask import request, jsonify

class InternshipController:
    @staticmethod
    def get_internships():
        internships = InternshipService.fetch_all_internships()
        return jsonify({"internships": internships})

    @staticmethod
    def create_internship():
        data = request.get_json()
        result = InternshipService.create_internship(data)
        return jsonify(result)

    @staticmethod
    def update_internship(internshipID):
        data = request.get_json()
        result = InternshipService.update_internship(internshipID, data)
        if "error" in result:
            return jsonify(result), 400 if result["error"] == "Internship not found" else 500
        return jsonify(result), 200
