
import os
os.environ["SECRET_KEY"] = "testsecret"

from main import app
from fastapi.testclient import TestClient

import uuid

client = TestClient(app)


def test_register():
    email = f"{uuid.uuid4().hex}@gmail.com"
    response = client.post(
        "/auth/register",
        json = {"email": email, "password": "123"}
    )
    assert response.status_code == 200



def test_show_my_accoutn_ok():
    email = "me_user_9@gmail.com."
    password =  "123"

#юзера создать
    client.post("/auth/register",
        json = {"email": "me_user_9@gmail.com.", "password": "123"})
#войти
    login = client.post("/auth/login",
        json = {"email": "me_user_9@gmail.com.", "password": "123"})
#окончательно войти aka token
    token = login.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers = {"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_wrong_login_ok():
    email = f"{uuid.uuid4().hex}@gmail.com"
    password = f"{uuid.uuid4().hex}"
    client.post(
        "/auth/register",
        json = {"email": email, "password": password}
    )
    response = client.post("/auth/login",
        json = {"email": email, "password": "неверный"}
    )
    assert response.status_code == 401



def test_create_product_ok():
    title = f"{uuid.uuid4()}"
    price = 100
    email = f"{uuid.uuid4().hex}@gmail.com" 
    password = f"{uuid.uuid4().hex}"

    client.post(
        "/auth/register",
        json = {"email": email, "password": password}
    )

    login = client.post(
        "/auth/login",
        json = {"email": email, "password": password}
    )
    token = login.json()["access_token"]

    response = client.post(
        "/products",
        json = {"price": price, "title": title},
        headers = {"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
