from flask import request, g
from functools import wraps
from app.utils.jwt_helper import decode_jwt

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return {"message": "Отсутствует токен авторизации"}, 401

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return {"message": "Неверный формат токена. Используйте Bearer <token>"}, 401

        token = parts[1]
        payload = decode_jwt(token)

        if not payload:
            return {"message": "Невалидный или просроченный токен"}, 401

        g.user_id = payload["user_id"]
        return func(*args, **kwargs)

    return wrapper

