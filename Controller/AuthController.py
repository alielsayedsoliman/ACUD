# Controller/AuthController.py
from BusinessLogic.Auth import AuthService
from flask import request, jsonify

class AuthController:
    @staticmethod
    def login():
        data = request.get_json()
        result = AuthService.login(data)
        return jsonify(result)
