from flask_restx import Resource, Namespace
from flask import g, request
from jinja2.compiler import generate
from werkzeug.security import check_password_hash, generate_password_hash

from app import User
from app.extensions.extensions import db
from app.utils.decorators import auth_required
from app.views.user import user_schema

profile_ns = Namespace("profile")

@profile_ns.route("/me")
class ProfileView(Resource):
    @auth_required
    def get(self):
        """
            Получить информацию о себе (нужно быть авторизованным)
        """
        user = User.query.get(g.user_id)
        return user_schema.dump(user), 200

    @auth_required
    def patch(self):
        """
            Обновить информацию о себе (нужно быть авторизованным)
        """
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
    def put(self, user_id):
        """
            Обновить пароль пользователя (нужно быть авторизированным)
        """
        user = User.query.get(user_id)
        if not user:
            return {"message": "пользователь не найден"}, 404

        data = request.get_json()
        password_1 = data.get("password_1") # старый пароль
        password_2 = data.get("password_2") # новый пароль

        if not password_1 or not password_2:
            return {"message": "Оба поля обязательны"}, 404

        if not check_password_hash(user.password, password_1):
            return {"massage": "Старый пароль неверный"}, 403

        user.password = generate_password_hash(password_2)
        db.session.commit()

        return '', 204
