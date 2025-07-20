from flask_restx import Resource, Namespace
from flask import request
from werkzeug.security import check_password_hash
from app.models.user import User
from app.utils.jwt_helper import generate_jwt
from werkzeug.security import generate_password_hash
from app.extensions.extensions import db

auth_ns = Namespace("auth")

@auth_ns.route("/register")
class RegisterView(Resource):
    def post(self):
        """
        Регистрация нового пользователя
        """
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        surname = data.get("surname")
        favorite_genre = data.get("favorite_genre")

        # Проверка обязательных полей
        if not email or not password:
            return {"message": "Email и пароль обязательны"}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "Пользователь уже существует"}, 400

        hashed_password = generate_password_hash(password)

        new_user = User(
            email=email,
            password=hashed_password,
            name=name,
            surname=surname,
            favorite_genre=favorite_genre
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "Пользователь зарегистрирован"}, 201

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


