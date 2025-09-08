from flask import Blueprint, request, jsonify
from Controller.Recruiter import RecruiterController

recruiter_bp = Blueprint("recruiter_bp", __name__)

@recruiter_bp.route("/recruiters", methods=["GET"])
def get_recruiters():
    page = request.args.get('page', default=1, type=int)
    items_per_page = request.args.get('items_per_page', default=10, type=int)

    if page < 1:
        return jsonify({"error": "Page number must be greater than 0"}), 400
    if items_per_page < 1:
        return jsonify({"error": "Items per page must be greater than 0"}), 400

    return RecruiterController.get_recruiters(page, items_per_page)

@recruiter_bp.route("/recruiters/register", methods=["POST"])
def register_recruiter():
    return RecruiterController.register_recruiter()
