def create_product(client, headers, title="Book", price=100):
    return client.post("/products", json={"title": title, "price": price}, headers=headers)


def test_create_product(client, make_user):
    response = create_product(client, make_user())
    assert response.status_code == 200
    assert response.json()["title"] == "Book"


def test_create_product_invalid_price(client, make_user):
    assert create_product(client, make_user(), price=0).status_code == 400


def test_list_only_my_products(client, make_user):
    alice, bob = make_user(), make_user()
    create_product(client, alice)
    assert len(client.get("/products", headers=alice).json()) == 1
    assert client.get("/products", headers=bob).json() == []


def test_cannot_delete_foreign_product(client, make_user):
    alice, bob = make_user(), make_user()
    product_id = create_product(client, alice).json()["id"]
    assert client.delete(f"/products/{product_id}", headers=bob).status_code == 403


def test_shop_hides_own_products(client, make_user):
    alice, bob = make_user(), make_user()
    create_product(client, alice)
    assert client.get("/shop", headers=alice).json() == []
    assert len(client.get("/shop", headers=bob).json()) == 1


def test_order_flow(client, make_user):
    seller, buyer = make_user(), make_user()
    product_id = create_product(client, seller).json()["id"]

    response = client.post(f"/order?product_id={product_id}", headers=buyer)
    assert response.status_code == 200
    assert response.json()["product_id"] == product_id

    orders = client.get("/order", headers=buyer).json()
    assert len(orders) == 1


def test_order_unknown_product(client, make_user):
    assert client.post("/order?product_id=999", headers=make_user()).status_code == 404


def test_cannot_order_own_product(client, make_user):
    seller = make_user()
    product_id = create_product(client, seller).json()["id"]
    assert client.post(f"/order?product_id={product_id}", headers=seller).status_code == 400


def test_cannot_order_twice(client, make_user):
    seller, buyer = make_user(), make_user()
    product_id = create_product(client, seller).json()["id"]
    client.post(f"/order?product_id={product_id}", headers=buyer)
    assert client.post(f"/order?product_id={product_id}", headers=buyer).status_code == 400


def test_shop_pagination(client, make_user):
    seller, buyer = make_user(), make_user()
    for i in range(5):
        create_product(client, seller, title=f"item {i}")

    first = client.get("/shop?limit=2&offset=0", headers=buyer).json()
    second = client.get("/shop?limit=2&offset=2", headers=buyer).json()
    last = client.get("/shop?limit=2&offset=4", headers=buyer).json()

    assert [len(first), len(second), len(last)] == [2, 2, 1]
    ids = [p["id"] for p in first + second + last]
    assert ids == sorted(set(ids))


def test_shop_pagination_limits(client, make_user):
    headers = make_user()
    assert client.get("/shop?limit=0", headers=headers).status_code == 422
    assert client.get("/shop?limit=101", headers=headers).status_code == 422
    assert client.get("/shop?offset=-1", headers=headers).status_code == 422


def test_delete_account_cascades(client, make_user):
    seller, buyer = make_user(), make_user()
    product_id = create_product(client, seller).json()["id"]
    client.post(f"/order?product_id={product_id}", headers=buyer)

    assert client.delete("/auth/me", headers=seller).status_code == 200

    # товар продавца удалился каскадом, вместе с ним и заказ покупателя
    assert client.get("/shop", headers=buyer).json() == []
    assert client.get("/order", headers=buyer).json() == []
    assert client.get("/auth/me", headers=seller).status_code == 401
