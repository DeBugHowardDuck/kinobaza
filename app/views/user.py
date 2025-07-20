from flask_restx import Resource, Namespace
from flask import request
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.schemas.user import UserRequestSchema, UserSchema
from app.extensions.extensions import db

user_ns =Namespace("users")
user_request_schema = UserRequestSchema()
user_schema = UserSchema()


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
        favorite_genre = data.get("favorite_genre")

        # Проверка на существование email
        if User.query.filter_by(email=email).first():
            return {"message": "пользователь с таким email уже существует"}, 400

        # Создание нового пользователя
        new_user = User(
            email=email,
            password=password,
            name=name,
            favorite_genre=favorite_genre
        )
        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201

    def patch(self):
        """
            Обновление информации о пользователи
        """
        data = request.get_json()

        email = data.get("email")

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "пользователь не найден"}, 404

        if "name" in data:
            user.name = data["name"]
        if "favorite_genre" in data:
            user.favorite_genre = data["favorite_genre"]

        db.session.commit()

        return user_schema(user), 200

