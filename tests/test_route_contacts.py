from unittest.mock import MagicMock, patch, AsyncMock

import pytest

from src.database.models import User
from src.services.auth import auth_service

CONTACT = {
    "first_name": "Test_User",
    "second_name": "Second_Test",
    "email": "test@gmail.com",
    "phone": "0996458844",
    "birth_date": "1993-01-01",   
    "user_id": 1
}


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)

    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={"username": user.get("email"),
                                                     "password": user.get("password")})
    data = response.json()
    return data["access_token"]



def test_get_contact(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get("/api/contacts",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list


def test_get_not_found_contact(client, token):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        response = client.get("/api/contacts/22",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Not Found"
        