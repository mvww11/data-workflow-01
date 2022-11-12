import pytest


def test_dummy():
    assert True


def test_index_route():
    app = pytest.importorskip("api.app").app
    response = app.test_client().get("/")

    assert response.status_code == 200
