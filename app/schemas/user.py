from marshmallow import Schema, fields
from app.schemas.genre import GenreSchema

class UserRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    name = fields.Str()
    favorite_genre = fields.Int()

class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    name = fields.Str()
    favorite_genre = fields.Int()
    genre = fields.Nested(GenreSchema)
