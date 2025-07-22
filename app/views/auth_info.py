from flask_restx import Resource, Namespace, fields
from flask import g, request
from werkzeug.security import check_password_hash, generate_password_hash

from app import User
from app.extensions.extensions import db, api
from app.utils.decorators import auth_required
from app.views.user import user_schema

profile_ns = Namespace("profile", description="Личный кабинет и смена пароля")

# Модели для Swagger
profile_update_model = api.model("ProfileUpdate", {
    "name": fields.String(description="Имя пользователя"),
    "surname": fields.String(description="Фамилия пользователя"),
    "favorite_genre": fields.Integer(description="ID любимого жанра")
})

password_update_model = api.model("PasswordUpdate", {
    "password_1": fields.String(required=True, description="Старый пароль"),
    "password_2": fields.String(required=True, description="Новый пароль")
})

error_model = api.model("Error", {
    "message": fields.String(description="Сообщение об ошибке")
})

user_model = api.model("UserResponse", {
    "id": fields.Integer,
    "email": fields.String,
    "name": fields.String,
    "surname": fields.String,
    "favorite_genre": fields.Integer
})


@profile_ns.route("/me")
class ProfileView(Resource):
    @auth_required
    @profile_ns.doc(description="Получить информацию о себе (нужна авторизация)")
    @profile_ns.response(200, "Успешно", user_model)
    def get(self):
        user = User.query.get(g.user_id)
        return user_schema.dump(user), 200

    @auth_required
    @profile_ns.expect(profile_update_model)
    @profile_ns.response(200, "Информация обновлена", user_model)
    @profile_ns.response(404, "Пользователь не найден", model=error_model)
    @profile_ns.doc(description="Обновить информацию о себе (нужна авторизация)")
    def patch(self):
        user = User.query.get(g.user_id)
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


@profile_ns.route("/password")
class PasswordUpdateView(Resource):
    @auth_required
    @profile_ns.expect(password_update_model)
    @profile_ns.response(204, "Пароль успешно обновлён")
    @profile_ns.response(403, "Старый пароль неверный", model=error_model)
    @profile_ns.response(404, "Пользователь не найден", model=error_model)
    @profile_ns.doc(description="Смена пароля (нужна авторизация)")
    def put(self):
        user = User.query.get(g.user_id)
        if not user:
            return {"message": "Пользователь не найден"}, 404

        data = request.get_json()
        password_1 = data.get("password_1")
        password_2 = data.get("password_2")

        if not password_1 or not password_2:
            return {"message": "Оба поля обязательны"}, 400

        if not check_password_hash(user.password, password_1):
            return {"message": "Старый пароль неверный"}, 403

        user.password = generate_password_hash(password_2)
        db.session.commit()

        return '', 204