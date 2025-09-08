# BusinessLogic/Auth.py
from Model.user import UserModel

class AuthService:
    @staticmethod
    def login(data):
        if "email" not in data or "password" not in data:
            return {"error": "Email and password are required"}
        return UserModel.login(data["email"], data["password"])
