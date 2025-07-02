from app.extensions.extensions import ma
from app.models.movie import Movie
from app.schemas.genre import GenreSchema
from app.schemas.director import DirectorSchema
from marshmallow import Schema, fields, validates, ValidationError, validates_schema
import datetime

class MovieSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Movie

    id = ma.auto_field()
    title = ma.auto_field(required=True)
    description = ma.auto_field()
    trailer = ma.auto_field()
    year = ma.auto_field(strict=True)
    rating = ma.auto_field()

    genre = ma.Nested(GenreSchema)
    director = ma.Nested(DirectorSchema)

class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class MovieRequestSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int(required=True)
    rating = fields.Float(required=True)
    genre_id = fields.Int()
    director_id = fields.Int(required=True)

    @validates_schema
    def validate_all(self, data, **kwargs):
        year = data.get("year")
        rating = data.get("rating")
        current_year = datetime.datetime.now().year

        if year is not None:
            if year > current_year:
                raise ValidationError("Год не может быть из будущего.", field_name="year")
            if year < 1888:
                raise ValidationError("Год слишком старый для фильма.", field_name="year")

        if rating is None:
            raise ValidationError("Рейтинг обязателен.", field_name="rating")
        if not (0 <= rating <= 10):
            raise ValidationError("Рейтинг должен быть от 0 до 10.", field_name="rating")

