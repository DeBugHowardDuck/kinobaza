from functools import wraps
from flask import request, g
import jwt
from app.qwe.config import Config
from app.models.user import User

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Отсутствует токен"}, 401

        try:
            token = token.replace("Bearer ", "")
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get("user_id")
        except Exception as e:
            return {"message": "Неверный или просроченный токен"}, 401

        user = User.query.get(user_id)
        if not user:
            return {"message": "Пользователь не найден"}, 404

        g.user = user  # сохраняем текущего пользователя
        return fn(*args, **kwargs)

    return wrapper