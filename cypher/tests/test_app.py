import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["model_loaded"] is True


@pytest.mark.parametrize("path", ["/", "/index", "/about", "/contact"])
def test_pages_render(client, path):
    assert client.get(path).status_code == 200


def test_static_css_served(client):
    r = client.get("/static/css/index.css")
    assert r.status_code == 200
    r.close()


def test_predict_returns_label(client):
    r = client.post("/check_url_api", json={"url": "https://github.com"})
    assert r.status_code == 200
    assert r.get_json()["prediction"] in ("Phishing", "Legitimate")


def test_predict_requires_url(client):
    assert client.post("/check_url_api", json={}).status_code == 400
    assert client.post("/check_url_api", data="not json").status_code == 400


def test_stats_increment(client):
    before = client.get("/get_dashboard_stats").get_json()["total"]
    client.post("/check_url_api", json={"url": "http://secure-login.example.com"})
    after = client.get("/get_dashboard_stats").get_json()["total"]
    assert after == before + 1
