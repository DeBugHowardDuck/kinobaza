from sqlalchemy import desc, asc

from app.models.movie import Movie
from app.extensions.extensions import db

class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Movie).all()

    def get_by_id(self, movie_id):
        return self.session.query(Movie).get(movie_id)

    def get_by_director(self, director_id):
        return self.session.query(Movie).filter(Movie.director_id == director_id).all()

    def get_by_genre(self, genre_id):
        return self.session.query(Movie).filter(Movie.genre_id == genre_id).all()

    def filter_movies(self, genre_id=None, director_id=None, sort_by=None):
        query = self.session.query(Movie)

        if genre_id:
            query = query.filter(Movie.genre_id == genre_id)
        if director_id:
            query = query.filter(Movie.director_id == director_id)

        if sort_by == "rating_desc":
            query = query.order_by(desc(Movie.rating))
        elif sort_by == "rating_asc":
            query = query.order_by(asc(Movie.rating))
        elif sort_by == "year_desc":
            query = query.order_by(desc(Movie.year))
        elif sort_by == "year_asc":
            query = query.order_by(asc(Movie.year))

        return query

    def create(self, data):
        new_movie = Movie(**data)
        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def save(self, movie):
        self.session.add(movie)
        self.session.commit()

    def delete(self, movie):
        self.session.delete(movie)
        self.session.commit()

    def search_by_title(self, keyword):
        return self.session.query(Movie).filter(Movie.title.ilike(f"%{keyword}%")).all()
