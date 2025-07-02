from app.models.user import User
from app.models.movie import Movie

class FavoritesDAO:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_movie(self, movie_id):
        return Movie.query.get(movie_id)

    def add_favorite(self, user, movie):
        user.favorites.append(movie)
        self.db_session.commit()

    def remove_favorite(self, user, movie):
        user.favorites.remove(movie)
        self.db_session.commit()