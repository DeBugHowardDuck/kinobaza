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

        if User.query.filter_by(email=email).first():
            return {"message": "пользователь с таким email уже существует"}, 400

        new_user = User(email=email, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201