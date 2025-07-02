from enum import unique

from sqlalchemy.orm import backref

from app.extensions.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    favorites = db.relationship(
        "Movie",
        secondary="favorites",
        backref="favorited_by"
    )