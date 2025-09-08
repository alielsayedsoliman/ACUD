from flask import Blueprint, request, jsonify
from Controller.mentorship_controller import request_mentor, get_assigned_students
from Model.mentorship import MentorshipModel


mentorship_bp = Blueprint("mentorship", __name__)

@mentorship_bp.route("/request", methods=["POST"])
def request_route():
    data = request.json
    studentID = data.get("studentID")
    mentorID = data.get("mentorID")

    response, status = request_mentor(studentID, mentorID)
    return jsonify(response), status

@mentorship_bp.route("/mentor/<mentorID>/requests", methods=["GET"])
def get_mentor_requests_route(mentorID):
    # Get pagination parameters from query string
    page = request.args.get('page', default=1, type=int)
    items_per_page = request.args.get('items_per_page', default=10, type=int)

    # Validate pagination parameters
    if page < 1:
        return jsonify({"error": "Page number must be greater than 0"}), 400
    if items_per_page < 1:
        return jsonify({"error": "Items per page must be greater than 0"}), 400

    response = MentorshipModel.get_mentor_requests(mentorID, page, items_per_page)
    if isinstance(response, dict) and "error" in response:
        return jsonify({"error": response["error"]}), 500
    return jsonify(response), 200

@mentorship_bp.route("/mentor/<mentorID>/students", methods=["GET"])
def assigned_students(mentorID):
    # Get pagination parameters from query string
    page = request.args.get('page', default=1, type=int)
    items_per_page = request.args.get('items_per_page', default=10, type=int)

    # Validate pagination parameters
    if page < 1:
        return jsonify({"error": "Page number must be greater than 0"}), 400
    if items_per_page < 1:
        return jsonify({"error": "Items per page must be greater than 0"}), 400

    response = MentorshipModel.get_mentor_students(mentorID, page, items_per_page)
    if isinstance(response, dict) and "error" in response:
        return jsonify({"error": response["error"]}), 500
    return jsonify(response), 200