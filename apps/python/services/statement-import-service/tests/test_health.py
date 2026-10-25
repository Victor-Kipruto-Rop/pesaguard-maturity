from fastapi.testclient import TestClient
from pesaguard_statement_import.app import app

def test_liveness() -> None:
    response = TestClient(app).get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
