class FavoritesService:
    def __init__(self, favorites_dao):
        self.favorites_dao = favorites_dao

    def get_user_favorites(self, user_id):
        user = self.favorites_dao.get_user(user_id)
        return user.favorites if user else None

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