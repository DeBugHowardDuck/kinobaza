from app.dao.genre_dao import GenreDAO

class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, genre_id):
        return self.dao.get_by_id(genre_id)

    def create(self, data):
        return self.dao.create(data)

    def update(self, genre_id, data):
        genre = self.dao.get_by_id(genre_id)
        if not genre:
            return None
        return self.dao.update(genre, data)

    def delete(self, genre_id):
        genre = self.dao.get_by_id(genre_id)
        if not genre:
            return False
        self.dao.delete(genre)
        return True