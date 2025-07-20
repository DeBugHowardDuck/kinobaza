import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions.extensions import db
from app.models.user import User
from app.utils.jwt_helper import generate_jwt


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
    """
    Получаем JWT-токен для авторизации
    """
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass"
    })
    return response.get_json()["token"]


@pytest.fixture
def created_movie(client, auth_token):
    """
    Создаём фильм перед тестами
    """
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


def test_create_movie_success(client, auth_token):
    movie_data = {
        "title": "Новый фильм",
        "description": "Описание фильма",
        "trailer": "https://youtube.com/test",
        "year": 2022,
        "rating": 8.5,
        "genre_id": 1,
        "director_id": 1
    }

    response = client.post("/movies/", json=movie_data, headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert response.status_code == 201
    assert response.get_json()["title"] == "Новый фильм"


def test_create_movie_unauthorized(client):
    movie_data = {
        "title": "Без токена",
        "description": "Не пустят",
        "trailer": "https://youtube.com/fail",
        "year": 2020,
        "rating": 5.5,
        "genre_id": 1,
        "director_id": 1
    }

    response = client.post("/movies/", json=movie_data)
    assert response.status_code == 401


def test_get_movies_list(client, created_movie):
    response = client.get("/movies/")
    data = response.get_json()

    assert response.status_code == 200
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1


def test_get_movie_by_id(client, created_movie):
    movie_id = created_movie["id"]
    response = client.get(f"/movies/{movie_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["title"] == "Фильм для теста"


def test_delete_movie(client, created_movie, auth_token):
    movie_id = created_movie["id"]
    response = client.delete(f"/movies/{movie_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "Фильм удалён"

    get_response = client.get(f"/movies/{movie_id}")
    assert get_response.status_code == 404

def test_update_movie_success(client, auth_token):
    movie_data = {
        "title": "Старое название",
        "description": "Описание",
        "trailer": "https://youtube.com/old",
        "year": 2001,
        "rating": 6.1,
        "genre_id": 1,
        "director_id": 1
    }

    create_response = client.post("/movies/", json=movie_data, headers={"Authorization": f"Bearer {auth_token}"})
    movie_id = create_response.json["id"]

    updated_data = {
        "title": "Новое название",
        "description": "Обновлённое описание",
        "trailer": "https://youtube.com/new",
        "year": 2020,
        "rating": 8.5,
        "genre_id": 1,
        "director_id": 1
    }

    update_response = client.put(f"/movies/{movie_id}", json=updated_data, headers={"Authorization": f"Bearer {auth_token}"})
    assert update_response.status_code == 200
    assert update_response.json["title"] == "Новое название"
    assert update_response.json["year"] == 2020


def test_update_movie_not_found(client, auth_token):
    update_data = {
        "title": "Не найдёшь",
        "description": "Пусто",
        "trailer": "https://youtube.com/none",
        "year": 2022,
        "rating": 7.0,
        "genre_id": 1,
        "director_id": 1
    }

    response = client.put("/movies/9999", json=update_data, headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert response.status_code == 404