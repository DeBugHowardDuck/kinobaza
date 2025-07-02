from app.models.director import Director
from app.extensions.extensions import db

class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Director).all()

    def get_by_id(self, director_id):
        return self.session.query(Director).get(director_id)

    def create(self, data):
        new_director = Director(**data)
        self.session.add(new_director)
        self.session.commit()
        return new_director

    def update(self, director, data):
        for key, value in data.items():
            setattr(director, key, value)
        self.session.commit()
        return director

    def delete(self, director):
        self.session.delete(director)
        self.session.commit()