from BusinessLogic.Recruiter import RecruiterService
from flask import request, jsonify

class RecruiterController:
    @staticmethod
    def get_recruiters(page=1, items_per_page=10):
        result = RecruiterService.fetch_all_recruiters(page, items_per_page)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result)

    @staticmethod
    def register_recruiter():
        data = request.get_json()
        result = RecruiterService.register_recruiter(data)
        return jsonify(result)
