def test_login_success(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert "token" in data


def test_login_wrong_password(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "неправильный"
    })

    assert response.status_code == 401
    assert response.get_json()["message"] == "Неверный пароль"


def test_login_user_not_found(client):
    response = client.post("/auth/login", json={
        "email": "noone@example.com",
        "password": "123"
    })

    assert response.status_code == 404
    assert response.get_json()["message"] == "Пользователь не найден"