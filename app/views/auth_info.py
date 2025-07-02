from flask_restx import Resource, Namespace
from flask import g
from app.utils.decorators import auth_required

profile_ns = Namespace("profile")

@profile_ns.route("/me")
class ProfileView(Resource):
    @auth_required
    def get(self):
        return {"message": f"Привет, пользователь с ID {g.user_id}"}