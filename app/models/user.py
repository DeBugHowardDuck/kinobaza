from app.extensions.extensions import db
from app.models.favorite import favorites

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100))
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genre.id"))

    favorites = db.relationship(
        "Movie",
        secondary="favorites",
        backref="favorited_by"
    )

    genre = db.relationship("Genre")