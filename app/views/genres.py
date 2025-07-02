from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from app.schemas.genre import GenreSchema, GenreRequestSchema
from app.dao.genre_dao import GenreDAO
from app.services.genre_service import GenreService
from app.extensions.extensions import db

genre_ns = Namespace("genres")
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)
genre_request_schema = GenreRequestSchema()

genre_dao = GenreDAO(db.session)
genre_service = GenreService(genre_dao)


@genre_ns.route('/')
class GenreListView(Resource):
    def get(self):
        """
        Получить все жанры
        """
        genres = genre_service.get_all()
        return genres_schema.dump(genres), 200

    def post(self):
        """
        Добавить жанр
        """
        data = request.get_json()
        try:
            validated_data = genre_request_schema.load(data)
        except ValidationError as e:
            return {"errors": e.messages}, 400

        new_genre = genre_service.create(validated_data)
        return genre_schema.dump(new_genre), 201


@genre_ns.route('/<int:genre_id>')
class GenreDetailView(Resource):
    def get(self, genre_id):
        """
        Получить жанр по ID
        """
        genre = genre_service.get_by_id(genre_id)
        if not genre:
            return {"message": "Жанр не найден"}, 404
        return genre_schema.dump(genre), 200

    def put(self, genre_id):
        """
        Обновить жанр
        """
        data = request.get_json()
        try:
            validated_data = genre_request_schema.load(data, partial=True)
        except ValidationError as e:
            return {"errors": e.messages}, 400

        updated_genre = genre_service.update(genre_id, validated_data)
        if not updated_genre:
            return {"message": "Жанр не найден"}, 404

        return genre_schema.dump(updated_genre), 200

    def delete(self, genre_id):
        """
        Удалить жанр
        """
        success = genre_service.delete(genre_id)
        if not success:
            return {"message": "Жанр не найден"}, 404
        return {"message": "Жанр удалён"}, 200