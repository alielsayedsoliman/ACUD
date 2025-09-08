from BusinessLogic.Mentor import MentorService
from flask import request, jsonify

class MentorController:
    @staticmethod
    def get_mentors():
        mentors = MentorService.fetch_all_mentors()
        return jsonify({"mentors": mentors})

    @staticmethod
    def register_mentor():
        data = request.get_json()
        result = MentorService.register_mentor(data)
        return jsonify(result)
