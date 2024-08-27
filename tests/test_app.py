from fastapi.testclient import TestClient
from fast_api.app import app

client = TestClient(app)
