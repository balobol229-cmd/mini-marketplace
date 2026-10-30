def test_register(client):
    response = client.post(
        "/auth/register", json={"email": "user@example.com", "password": "password123"}
    )
    assert response.status_code == 200


def test_register_duplicate_email(client):
    body = {"email": "user@example.com", "password": "password123"}
    client.post("/auth/register", json=body)
    assert client.post("/auth/register", json=body).status_code == 400


def test_register_short_password(client):
    response = client.post(
        "/auth/register", json={"email": "user@example.com", "password": "123"}
    )
    assert response.status_code == 422


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register", json={"email": "not-an-email", "password": "password123"}
    )
    assert response.status_code == 422


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "user@example.com", "password": "password123"})
    response = client.post(
        "/auth/login", json={"email": "user@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_me(client, make_user):
    response = client.get("/auth/me", headers=make_user())
    assert response.status_code == 200
    assert "password" not in response.json()


def test_me_without_token(client):
    assert client.get("/auth/me").status_code in (401, 403)


def test_me_invalid_token(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer garbage"})
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
