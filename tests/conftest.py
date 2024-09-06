import pytest
from fastapi.testclient import TestClient
from fast_api.app import app


@pytest.fixture(autouse=True)
def client():
    return TestClient(app)
