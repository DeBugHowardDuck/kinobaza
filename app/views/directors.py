

from flask import request
from flask_restx import Resource, Namespace, fields
from marshmallow import ValidationError

from app.schemas.director import DirectorSchema, DirectorRequestSchema
from app.dao.director_dao import DirectorDAO
from app.services.director_service import DirectorService
from app.extensions.extensions import db, api

director_model = api.model("DirectorRequest", {
    "name": fields.String(required=True, description="Имя режиссёра")
})

director_response_model = api.model("DirectorResponse", {
    "id": fields.Integer(description="ID режиссёра"),
    "name": fields.String(description="Имя режиссёра")
})

error_model = api.model("Error", {
    "message": fields.String(description="Сообщение об ошибке")
})

director_ns = Namespace("directors")
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
director_request_schema = DirectorRequestSchema()

# Подключаем DAO и Service
director_dao = DirectorDAO(db.session)
director_service = DirectorService(director_dao)


@director_ns.route('/')
class DirectorListView(Resource):
    @director_ns.doc(description="Получить всех режиссёров")
    @director_ns.marshal_list_with(director_response_model)
    def get(self):
        """
        Получить всех режиссёров
        """
        directors = director_service.get_all()
        return directors_schema.dump(directors), 200

    @director_ns.doc(description="Добавить нового режиссёра")
    @api.expect(director_model)
    @api.marshal_with(director_response_model, code=201)
    @api.response(400, "Ошибка валидации", model=error_model)
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
    @director_ns.doc(description="Получить режиссёра по ID")
    @api.marshal_with(director_response_model)
    @api.response(404, "Режиссёр не найден", model=error_model)
    def get(self, director_id):
        """
        Получить режиссёра по ID
        """
        director = director_service.get_by_id(director_id)
        if not director:
            return {"message": "Режиссёр не найден"}, 404
        return director_schema.dump(director), 200

    @director_ns.doc(description="Обновить режиссёра")
    @api.expect(director_model)
    @api.marshal_with(director_response_model)
    @api.response(400, "Ошибка валидации", model=error_model)
    @api.response(404, "Режиссёр не найден", model=error_model)
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

    @director_ns.doc(description="Удалить режиссёра")
    @api.response(200, "Режиссёр удалён")
    @api.response(404, "Режиссёр не найден", model=error_model)
    def delete(self, director_id):
        """
        Удалить режиссёра
        """
        success = director_service.delete(director_id)
        if not success:
            return {"message": "Режиссёр не найден"}, 404

        return {"message": "Режиссёр удалён"}, 200