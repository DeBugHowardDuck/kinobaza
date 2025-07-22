from flask_restx import Resource, Namespace, fields
from flask import request
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.utils.jwt_helper import generate_jwt
from app.extensions.extensions import db, api

auth_ns = Namespace("auth", description="Аутентификация")

auth_model = api.model("AuthRequest", {
    "email": fields.String(required=True, description="Email пользователя"),
    "password": fields.String(required=True, description="Пароль пользователя"),
})

token_response_model = api.model("TokenResponse", {
    "access_token": fields.String(description="JWT access token")
})

error_model = api.model("Error", {
    "message": fields.String(description="Сообщение об ошибке")
})

register_model = api.model("RegisterRequest", {
    "email": fields.String(required=True, description="Email пользователя"),
    "password": fields.String(required=True, description="Пароль"),
    "name": fields.String(description="Имя"),
    "surname": fields.String(description="Фамилия"),
    "favorite_genre": fields.Integer(description="ID любимого жанра"),
})


@auth_ns.route("/register")
class RegisterView(Resource):
    @auth_ns.doc(description="Регистрация нового пользователя")
    @auth_ns.expect(register_model)
    @auth_ns.response(201, "Пользователь зарегистрирован")
    @auth_ns.response(400, "Некорректные данные", model=error_model)
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
    @auth_ns.doc(description="Вход пользователя. Возвращает JWT access token.")
    @auth_ns.expect(auth_model)
    @auth_ns.response(200, "Успешный вход", token_response_model)
    @auth_ns.response(400, "Ошибка валидации", model=error_model)
    @auth_ns.response(401, "Неверные учетные данные", model=error_model)
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
        return {"access_token": token}, 200


