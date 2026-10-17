import pytest

from app import create_app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    import app as app_module

    monkeypatch.setattr(app_module, "DATABASE", tmp_path / "test.db")
    application = create_app({"TESTING": True, "SECRET_KEY": "test-key"})
    with application.test_client() as test_client:
        yield test_client


def test_homepage_shows_products(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"NOVA" in response.data
    assert b"Everyday Bottle" in response.data


def test_search_filters_products(client):
    response = client.get("/?q=headphones")
    assert response.status_code == 200
    assert b"Wireless Headphones" in response.data
    assert b"Everyday Bottle" not in response.data


def test_add_to_cart_and_view_cart(client):
    response = client.post("/cart/add/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Everyday Bottle" in response.data
    assert client.get("/cart").status_code == 200


def test_unknown_product_returns_404(client):
    assert client.post("/cart/add/9999").status_code == 404


def test_checkout_saves_order(client):
    client.post("/cart/add/1")
    response = client.post(
        "/checkout",
        data={"name": "Test Student", "email": "test@example.com"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Order Confirmed" in response.data
    assert b"Thanks, Test Student" in response.data


def test_checkout_rejects_invalid_email(client):
    client.post("/cart/add/1")
    response = client.post(
        "/checkout", data={"name": "Test Student", "email": "invalid"})
    assert response.status_code == 200
    assert b"Enter a valid name and email" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
