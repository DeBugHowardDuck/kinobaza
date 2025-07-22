from flask_restx import Resource, Namespace, fields
from flask import g, request
from app.utils.decorators import auth_required
from app.services.favorites_service import FavoritesService
from app.dao.favorites_dao import FavoritesDAO
from app.extensions.extensions import db, api
from app.schemas.movie import MovieSchema

favorites_ns = Namespace("favorites", description="Работа с избранными фильмами")

favorites_dao = FavoritesDAO(db.session)
favorites_service = FavoritesService(favorites_dao)

movie_schema = MovieSchema(many=True)

movie_response_model = api.model("MovieResponse", {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "trailer": fields.String,
    "year": fields.Integer,
    "rating": fields.Float,
    "genre_id": fields.Integer,
    "director_id": fields.Integer
})

error_model = api.model("Error", {
    "message": fields.String(description="Сообщение об ошибке")
})


@favorites_ns.route("/")
class FavoritesListView(Resource):
    @auth_required
    @favorites_ns.doc(description="Получить список избранных фильмов пользователя",
                      params={
                          "page": "Номер страницы",
                          "per_page": "Количество элементов на странице"
                      })
    @favorites_ns.response(200, "Список избранного получен")
    def get(self):
        user_id = g.user_id
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        result = favorites_service.get_user_favorites(user_id, page, per_page)

        return {
            "page": result["page"],
            "per_page": result["per_page"],
            "total_page": result["total_page"],
            "total_items": result["total_items"],
            "items": movie_schema.dump(result["items"])
        }, 200


@favorites_ns.route("/<int:movie_id>")
class FavoriteView(Resource):
    @auth_required
    @favorites_ns.doc(description="Добавить фильм в избранное")
    @favorites_ns.response(201, "Фильм добавлен в избранное")
    @favorites_ns.response(404, "Фильм не найден", model=error_model)
    def post(self, movie_id):
        return favorites_service.add_to_favorites(g.user_id, movie_id)

    @auth_required
    @favorites_ns.doc(description="Удалить фильм из избранного")
    @favorites_ns.response(200, "Фильм удалён из избранного")
    @favorites_ns.response(404, "Фильм не найден", model=error_model)
    def delete(self, movie_id):
        return favorites_service.remove_from_favorites(g.user_id, movie_id)