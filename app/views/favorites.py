from flask_restx import Resource, Namespace
from flask import g
from app.utils.decorators import auth_required
from app.services.favorites_service import FavoritesService
from app.dao.favorites_dao import FavoritesDAO
from app.extensions.extensions import db
from app.schemas.movie import MovieSchema

favorites_ns = Namespace("favorites")
favorites_dao = FavoritesDAO(db.session)
favorites_service = FavoritesService(favorites_dao)
movie_schema = MovieSchema(many=True)

@favorites_ns.route("/")
class FavoritesListView(Resource):
    @auth_required
    def get(self):
        favorites = favorites_service.get_user_favorites(g.user_id)
        if favorites is None:
            return {"message": "Пользователь не найден"}, 404
        return movie_schema.dump(favorites), 200

@favorites_ns.route("/<int:movie_id>")
class FavoriteView(Resource):
    @auth_required
    def post(self, movie_id):
        return favorites_service.add_to_favorites(g.user_id, movie_id)

    @auth_required
    def delete(self, movie_id):
        return favorites_service.remove_from_favorites(g.user_id, movie_id)