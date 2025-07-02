from app.dao.movie_dao import MovieDAO
from math import ceil

class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_all(self, director_id=None, genre_id=None):
        if director_id:
            return self.dao.get_by_director(director_id)
        if genre_id:
            return self.dao.get_by_genre(genre_id)
        return self.dao.get_all()

    def get_by_id(self, movie_id):
        return self.dao.get_by_id(movie_id)

    def get_filtered_movies(self, genre_id=None, director_id=None, sort_by=None, page=1, per_page=10):
        query = self.dao.filter_movies(genre_id, director_id, sort_by)
        total_items = query.count()
        total_pages = ceil(total_items / per_page)
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "items": items
        }

    def create_movie(self, data):
        new_movie = self.dao.create(data)
        return new_movie

    def update_movie(self, movie_id, data):
        movie = self.dao.get_by_id(movie_id)
        if not movie:
            return None
        for key, value in data.items():
            setattr(movie, key, value)
        self.dao.save(movie)
        return movie

    def delete_movie(self, movie_id):
        movie = self.dao.get_by_id(movie_id)
        if not movie:
            return False
        self.dao.delete(movie)
        return True

    def search_movies(self, keyword):
        return self.dao.search_by_title(keyword)

