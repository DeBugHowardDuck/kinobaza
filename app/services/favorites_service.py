from math import ceil

class FavoritesService:
    def __init__(self, favorites_dao):
        self.favorites_dao = favorites_dao

    def get_user_favorites(self, user_id, page=1, per_page=10):
        user = self.favorites_dao.get_user_by_id(user_id)
        if not user:
            return {"items": [], "page": page, "per_page": per_page, "total_pages": 0, "total_items": 0}
        favorites = user.favorites
        total_items = len(favorites)
        total_pages = ceil(total_items / per_page)

        start = (page-1) * per_page
        end = start + per_page
        paginated_items = favorites[start:end]

        return {
            "items": paginated_items,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_items": total_items
        }


    def add_to_favorites(self, user_id, movie_id):
        user = self.favorites_dao.get_user(user_id)
        movie = self.favorites_dao.get_movie(movie_id)

        if not user:
            return {"message": "Пользователь не найден"}, 404
        if not movie:
            return {"message": "Фильм не найден"}, 404
        if movie in user.favorites:
            return {"message": "Фильм уже в избранном"}, 409

        self.favorites_dao.add_favorite(user, movie)
        return {"message": f"Фильм '{movie.title}' добавлен"}, 201

    def remove_from_favorites(self, user_id, movie_id):
        user = self.favorites_dao.get_user(user_id)
        movie = self.favorites_dao.get_movie(movie_id)

        if not user or not movie:
            return {"message": "Фильм или пользователь не найден"}, 404
        if movie not in user.favorites:
            return {"message": "Фильм не в избранном"}, 404

        self.favorites_dao.remove_favorite(user, movie)
        return {"message": f"Фильм '{movie.title}' удалён из избранного"}, 200