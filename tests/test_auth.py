import pytest
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

# Предполагается, что у вас есть фикстура client, как в ваших примерах
# Если нет, то она может выглядеть примерно так (в conftest.py):

# @pytest.fixture(scope="module")
# def client():
#     app = create_app()
#     app.config["TESTING"] = True
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:" # Использование in-memory базы данных для тестов
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#             # Создаем тестового пользователя для входа
#             hashed_password = generate_password_hash("testpassword")
#             user = User(email="test@example.com", password=hashed_password, name="Тестовый", surname="Пользователь")
#             db.session.add(user)
#             db.session.commit()
#         yield client
#         with app.app_context():
#             db.drop_all()

def test_login_success(client):
    """Тест успешного входа пользователя."""
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert "access_token" in data, "При успешном входе должен возвращаться access_token"


def test_login_wrong_password(client):
    """Тест входа с неверным паролем."""
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert "message" in response.get_json()
    assert response.get_json()["message"] == "Неверные учётные данные", \
        "Сообщение для неверного пароля должно быть 'Неверные учётные данные'"


def test_login_nonexistent_user(client):
    """Тест входа для несуществующего пользователя."""
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "any-password"
    })

    assert response.status_code == 401
    assert "message" in response.get_json()
    assert response.get_json()["message"] == "Неверные учётные данные", \
        "Сообщение для несуществующего пользователя должно быть 'Неверные учётные данные'"


def test_login_missing_data(client):
    """Тест входа с отсутствующими данными."""
    response = client.post("/auth/login", json={})

    assert response.status_code == 400
    assert "message" in response.get_json()
    assert response.get_json()["message"] == "Email и пароль обязательны", \
        "Сообщение для отсутствующих данных при входе должно быть 'Email и пароль обязательны'"


def test_register_success(client):
    """Тест успешной регистрации нового пользователя."""
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "newpassword",
        "name": "Новый",  # <-- Добавлено обязательное поле name
        "surname": "Пользователь" # <-- Можно добавить, если surname тоже NOT NULL
    })

    assert response.status_code == 201
    assert "message" in response.get_json()
    assert response.get_json()["message"] == "Пользователь успешно зарегистрирован", \
        "Сообщение об успешной регистрации неверно"


def test_register_existing_email(client):
    """Тест регистрации с уже существующим email."""
    # Регистрируем пользователя для теста
    client.post("/auth/register", json={
        "email": "already@used.com",
        "password": "secret",
        "name": "Существующий", # <-- Добавлено обязательное поле name
        "surname": "Пользователь" # <-- Можно добавить, если surname тоже NOT NULL
    })

    # Повторно пытаемся зарегистрировать того же пользователя
    response = client.post("/auth/register", json={
        "email": "already@used.com",
        "password": "secret",
        "name": "Дубликат", # <-- Добавлено обязательное поле name
        "surname": "Пользователь" # <-- Можно добавить, если surname тоже NOT NULL
    })

    assert response.status_code == 409
    assert "message" in response.get_json()
    assert response.get_json()["message"] == "Пользователь с таким email уже существует", \
        "Сообщение для существующего email неверно"


def test_register_missing_data(client):
    """Тест регистрации с отсутствующими данными."""
    response = client.post("/auth/register", json={})

    assert response.status_code == 400
    assert "message" in response.get_json()
    assert response.get_json()["message"] == "Email и пароль обязательны", \
        "Сообщение для отсутствующих данных при регистрации неверно"