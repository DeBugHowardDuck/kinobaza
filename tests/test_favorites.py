import pytest

#Добавление в избранное
def test_add_favorite_success(client, auth_token, created_movie):
    movie_id = created_movie["id"]
    response = client.post(f"/favorites/{movie_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert response.status_code == 201
    expected_message = f"Фильм '{created_movie['title']}' добавлен"
    assert response.get_json()["message"] == expected_message

#Попытка добавить без токена
def test_add_favorite_unauthorized(client, created_movie):
    movie_id = created_movie["id"]
    response = client.post(f"/favorites/{movie_id}")
    assert response.status_code == 401

#Получение списка избранного
def test_get_favorites(client, auth_token, created_movie):
    movie_id = created_movie["id"]

    # Сначала добавим фильм
    client.post(f"/favorites/{movie_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    # Получим список
    response = client.get("/favorites/", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(movie["id"] == movie_id for movie in data)

#Удаление из избранного
def test_delete_favorite_success(client, auth_token, created_movie):
    movie_id = created_movie["id"]

    # Сначала добавим
    client.post(f"/favorites/{movie_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    # Удалим
    response = client.delete(f"/favorites/{movie_id}", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert response.status_code == 200
    expected_message = f"Фильм '{created_movie['title']}' удалён из избранного"
    assert response.get_json()["message"] == expected_message

#Удаление без токена
def test_delete_favorite_unauthorized(client, created_movie):
    movie_id = created_movie["id"]
    response = client.delete(f"/favorites/{movie_id}")
    assert response.status_code == 401