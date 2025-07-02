from app.extensions.extensions import ma
from app.models.director import Director
from marshmallow import Schema, fields

class DirectorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Director

    id = ma.auto_field()
    name = ma.auto_field()

class DirectorRequestSchema(Schema):
    name = fields.Str(required=True)