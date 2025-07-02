from app.dao.director_dao import DirectorDAO

class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, director_id):
        return self.dao.get_by_id(director_id)

    def create(self, data):
        return self.dao.create(data)

    def update(self, director_id, data):
        director = self.dao.get_by_id(director_id)
        if not director:
            return None
        return self.dao.update(director, data)

    def delete(self, director_id):
        director = self.dao.get_by_id(director_id)
        if not director:
            return False
        self.dao.delete(director)
        return True