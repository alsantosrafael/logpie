import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from logpie.middleware import LoggingMiddleware


@pytest.fixture
def app():
    app = FastAPI()
    app.add_middleware(LoggingMiddleware)

    @app.get("/ping")
    async def ping():
        return {"message": "pong"}

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_middleware_adds_request_id(client):
    """Middleware should inject request_id header into logs context."""
    response = client.get("/ping")
    assert response.status_code == 200
    assert "x-request-id" in response.headers


def test_middleware_preserves_custom_request_id(client):
    """Middleware should respect user-provided x-request-id header."""
    custom_id = "my-custom-id-123"
    response = client.get("/ping", headers={"x-request-id": custom_id})
    assert response.status_code == 200
    assert response.headers["x-request-id"] == custom_id
