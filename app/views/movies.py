from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError
from flask_restx import fields
from app.dao.movie_dao import MovieDAO
from app.models.movie import Movie
from app.schemas.movie import MovieSchema
from app.extensions.extensions import db, api
from sqlalchemy import desc, asc
from app.schemas.movie import MovieRequestSchema
from math import ceil
import logging
from app.services.movie_service import MovieService
from app.utils.decorators import auth_required



movie_ns = Namespace("movies")
movie_request_schema = MovieRequestSchema()
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

logger = logging.getLogger(__name__)

movie_dao = MovieDAO(db.session)
movie_service = MovieService(movie_dao)

movie_model = api.model("MovieRequest", {
    "title": fields.String(required=True, description="Название фильма"),
    "description": fields.String(description="Описание"),
    "trailer": fields.String(description="Ссылка на трейлер"),
    "year": fields.Integer(required=True, description="Год выпуска"),
    "rating": fields.Float(required=True, description="Рейтинг от 0 до 10"),
    "genre_id": fields.Integer(description="ID жанра"),
    "director_id": fields.Integer(required=True, description="ID режиссёра")
})


@movie_ns.route('/')
class MovieListView(Resource):
    def get(self):
        """
        Получить список фильмов с фильтрацией, сортировкой и пагинацией
        """
        genre_id = request.args.get('genre_id', type=int)
        director_id = request.args.get('director_id', type=int)
        sort_by = request.args.get('sort_by')
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        logger.debug(f"GET /movies — page={page}, per_page={per_page}, director={director_id}, genre={genre_id}, sort={sort_by}")

        result = movie_service.get_filtered_movies(
            genre_id=genre_id,
            director_id=director_id,
            sort_by=sort_by,
            page=page,
            per_page=per_page
        )

        return {
            "page": result["page"],
            "per_page": result["per_page"],
            "total_pages": result["total_pages"],
            "total_items": result["total_items"],
            "items": movies_schema.dump(result["items"])
        }, 200

    @auth_required
    @api.expect(movie_model)
    def post(self):
        """
        Добавить новый фильм
        """
        data = request.get_json()
        try:
            validated_data = movie_request_schema.load(data)
        except ValidationError as e:
            return {"errors": e.messages}, 400

        new_movie = movie_service.create_movie(validated_data)
        return movie_schema.dump(new_movie), 201

@movie_ns.route('/<int:movie_id>')
class MovieDetailView(Resource):
    def get(self, movie_id):
        """
            Получить один фильм по ID
        """
        movie = Movie.query.get(movie_id)
        if movie is None:
            return {"massage": "Кина не будет"}, 404
        return MovieSchema().dump(movie), 200

    @auth_required
    def put(self, movie_id):
        """
        Обновить данные фильма
        """
        data = request.get_json()
        try:
            validated_data = movie_request_schema.load(data, partial=True)
        except ValidationError as e:
            return {"errors": e.messages}, 400

        updated_movie = movie_service.update_movie(movie_id, validated_data)
        if not updated_movie:
            return {"message": "Фильм не найден"}, 404

        return movie_schema.dump(updated_movie), 200

    @auth_required
    def delete(self, movie_id):
        """
        Удалить фильм
        """
        success = movie_service.delete_movie(movie_id)
        if not success:
            return {"message": "Фильм не найден"}, 404
        return {"message": "Фильм удалён"}, 200

@movie_ns.route("/search")
class MovieSearchView(Resource):
    def get(self):
        """
        Поиск фильмов по ключевому слову в названии
        """
        keyword = request.args.get("q", "")

        if not keyword:
            return {"message": "Не задан параметр 'q'"}, 400

        movies = movie_service.search_movies(keyword)
        return movies_schema.dump(movies), 200
