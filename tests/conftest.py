import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions.extensions import db
from app.models.user import User

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Создаём пользователя
        user = User(email="test@example.com", password=generate_password_hash("testpass"), name="Test")
        db.session.add(user)
        db.session.commit()

    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_token(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass"
    })
    return response.get_json()["token"]

@pytest.fixture
def created_movie(client, auth_token):
    movie_data = {
        "title": "Фильм для теста",
        "description": "Описание",
        "trailer": "https://youtube.com/test",
        "year": 2023,
        "rating": 7.8,
        "genre_id": 1,
        "director_id": 1
    }

    response = client.post("/movies/", json=movie_data, headers={
        "Authorization": f"Bearer {auth_token}"
    })

    return response.get_json()