from flask_restx import Resource, Namespace
from flask import request
from werkzeug.security import check_password_hash
from app.models.user import User
from app.utils.jwt_helper import generate_jwt

auth_ns = Namespace("auth")

@auth_ns.route("/login")
class LoginView(Resource):
    def post(self):
        """
            Логин пользователя, возвращает JWT-токен
        """
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email и пароль обязательны"}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "Пользователь не найден"}, 404

        if not check_password_hash(user.password, password):
            return {"message": "Неверный пароль"}, 401

        token = generate_jwt(user.id)
        return {"token": token}, 200
