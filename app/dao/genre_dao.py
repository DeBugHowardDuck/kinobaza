from app.models.genre import Genre
from app.extensions.extensions import db

class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Genre).all()

    def get_by_id(self, genre_id):
        return self.session.query(Genre).get(genre_id)

    def create(self, data):
        new_genre = Genre(**data)
        self.session.add(new_genre)
        self.session.commit()
        return new_genre

    def update(self, genre, data):
        for key, value in data.items():
            setattr(genre, key, value)
        self.session.commit()
        return genre

    def delete(self, genre):
        self.session.delete(genre)
        self.session.commit()