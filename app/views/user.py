from flask_restx import Resource, Namespace, fields
from flask import request
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.schemas.user import UserRequestSchema, UserSchema
from app.extensions.extensions import db, api
from app.utils.jwt_helper import decode_jwt

user_ns = Namespace("users")
user_request_schema = UserRequestSchema()
user_schema = UserSchema()


user_response_model = api.model("UserResponse", {
    "id": fields.Integer(description="ID пользователя"),
    "email": fields.String(description="Email"),
    "name": fields.String(description="Имя"),
    "surname": fields.String(description="Фамилия"),
    "favorite_genre": fields.Integer(description="ID любимого жанра"),
})

error_model = api.model("Error", {
    "message": fields.String(description="Сообщение об ошибке")
})


@user_ns.route("/")
class UserRegisterView(Resource):
    def post(self):
        """
        Регистрация нового пользователя
        """
        data = request.get_json()

        errors = user_request_schema.validate(data)
        if errors:
            return {"errors": errors}, 400

        email = data["email"]
        password = generate_password_hash(data["password"])
        name = data.get("name")
        surname = data.get("surname")
        favorite_genre = data.get("favorite_genre")

        if User.query.filter_by(email=email).first():
            return {"message": "Пользователь с таким email уже существует"}, 400

        new_user = User(
            email=email,
            password=password,
            name=name,
            surname=surname,
            favorite_genre=favorite_genre
        )
        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201

    def patch(self):
        """
        Обновление информации о пользователе
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"message": "Токен отсутствует или некорректен"}, 401

        token = auth_header.split(" ")[1]
        payload = decode_jwt(token)

        if not payload:
            return {"message": "Невалидный или истёкший токен"}, 401

        user = User.query.get(payload["user_id"])
        if not user:
            return {"message": "Пользователь не найден"}, 404

        data = request.get_json()

        if "name" in data:
            user.name = data["name"]
        if "surname" in data:
            user.surname = data["surname"]
        if "favorite_genre" in data:
            user.favorite_genre = data["favorite_genre"]

        db.session.commit()
        return user_schema.dump(user), 200


@user_ns.route("/me")
class UserProfileView(Resource):
    @user_ns.doc(description="Получить профиль текущего пользователя")
    @user_ns.response(200, "Успешно", user_response_model)
    @user_ns.response(401, "Токен невалиден", model=error_model)
    def get(self):
        """
        Получить данные текущего пользователя по JWT
        """
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return {"message": "Токен отсутствует или некорректен"}, 401

        token = auth_header.split(" ")[1]
        payload = decode_jwt(token)

        if not payload:
            return {"message": "Токен недействителен или истёк"}, 401

        user_id = payload["user_id"]
        user = User.query.get(user_id)

        if not user:
            return {"message": "Пользователь не найден"}, 404

        return user_schema.dump(user), 200