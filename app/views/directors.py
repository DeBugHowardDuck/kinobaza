# app/views/directors.py

from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from app.schemas.director import DirectorSchema, DirectorRequestSchema
from app.dao.director_dao import DirectorDAO
from app.services.director_service import DirectorService
from app.extensions.extensions import db

director_ns = Namespace("directors")
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
director_request_schema = DirectorRequestSchema()

# Подключаем DAO и Service
director_dao = DirectorDAO(db.session)
director_service = DirectorService(director_dao)


@director_ns.route('/')
class DirectorListView(Resource):
    def get(self):
        """
        Получить всех режиссёров
        """
        directors = director_service.get_all()
        return directors_schema.dump(directors), 200

    def post(self):
        """
        Добавить нового режиссёра
        """
        data = request.get_json()
        try:
            validated_data = director_request_schema.load(data)
        except ValidationError as e:
            return {"errors": e.messages}, 400

        new_director = director_service.create(validated_data)
        return director_schema.dump(new_director), 201


@director_ns.route('/<int:director_id>')
class DirectorDetailView(Resource):
    def get(self, director_id):
        """
        Получить режиссёра по ID
        """
        director = director_service.get_by_id(director_id)
        if not director:
            return {"message": "Режиссёр не найден"}, 404
        return director_schema.dump(director), 200

    def put(self, director_id):
        """
        Обновить данные режиссёра
        """
        data = request.get_json()
        try:
            validated_data = director_request_schema.load(data, partial=True)
        except ValidationError as e:
            return {"errors": e.messages}, 400

        updated = director_service.update(director_id, validated_data)
        if not updated:
            return {"message": "Режиссёр не найден"}, 404

        return director_schema.dump(updated), 200

    def delete(self, director_id):
        """
        Удалить режиссёра
        """
        success = director_service.delete(director_id)
        if not success:
            return {"message": "Режиссёр не найден"}, 404

        return {"message": "Режиссёр удалён"}, 200