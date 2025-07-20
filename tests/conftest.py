import pytest
from app import create_app
from app.extensions.extensions import db
from app.models.user import User
from app.models.genre import Genre
from app.models.director import Director
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Добавим жанр и режиссёра
        genre = Genre(name="Драма")
        director = Director(name="Кристофер Нолан")
        db.session.add_all([genre, director])
        db.session.commit()

        # Создаём пользователя
        user = User(
            email="test@example.com",
            password=generate_password_hash("testpass"),
            name="Тестовый Пользователь"
        )
        db.session.add(user)
        db.session.commit()

    with app.test_client() as client:
        yield client