from app.extensions.extensions import ma
from app.models.genre import Genre
from marshmallow import Schema, fields

class GenreSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Genre

    id = ma.auto_field()
    name = ma.auto_field()

class GenreRequestSchema(Schema):
    name = fields.Str(required=True)
