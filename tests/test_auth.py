import json
import jwt
from datetime import datetime, timedelta, timezone


class TestSignup:
    def test_signup_success(self, client):
        response = client.post(
            "/api/auth/signup",
            json={"email": "newuser@example.com", "password": "password123"},
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert "access" in data
        assert "refresh" in data
        assert isinstance(data["access"], str)
        assert isinstance(data["refresh"], str)

    def test_signup_duplicate_email(self, client, test_user):
        response = client.post(
            "/api/auth/signup",
            json={"email": test_user.email, "password": "password123"},
        )

        assert response.status_code == 400

    def test_signup_missing_email(self, client):
        response = client.post(
            "/api/auth/signup",
            json={"password": "password123"},
        )

        assert response.status_code == 400

    def test_signup_missing_password(self, client):
        response = client.post(
            "/api/auth/signup",
            json={"email": "test@example.com"},
        )

        assert response.status_code == 400

    def test_signup_invalid_email_format(self, client):
        # Current implementation doesn't validate email format
        response = client.post(
            "/api/auth/signup",
            json={"email": "not-an-email", "password": "password123"},
        )

        assert response.status_code == 201


class TestLogin:
    def test_login_success(self, client, test_user):
        response = client.post(
            "/api/auth/login",
            json={"email": test_user.email, "password": "password123"},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "access" in data
        assert "refresh" in data
        assert isinstance(data["access"], str)
        assert isinstance(data["refresh"], str)

    def test_login_invalid_email(self, client):
        response = client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"},
        )

        assert response.status_code == 401

    def test_login_invalid_password(self, client, test_user):
        response = client.post(
            "/api/auth/login",
            json={"email": test_user.email, "password": "wrongpassword"},
        )

        assert response.status_code == 401

    def test_login_missing_email(self, client):
        response = client.post(
            "/api/auth/login",
            json={"password": "password123"},
        )

        assert response.status_code == 400

    def test_login_missing_password(self, client):
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com"},
        )

        assert response.status_code == 400


class TestRefresh:
    def test_refresh_success(self, client, refresh_token):
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "access" in data
        assert "refresh" in data
        assert isinstance(data["access"], str)
        assert isinstance(data["refresh"], str)
        assert data["access"] != data["refresh"]

    def test_refresh_missing_authorization_header(self, client):
        response = client.post("/api/auth/refresh")

        assert response.status_code == 401

    def test_refresh_invalid_token_format(self, client):
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": "Bearer invalid.token.here"},
        )

        assert response.status_code == 401

    def test_refresh_expired_token(self, client, test_user):
        from arvo.config import config
        from arvo.services.auth import TokenType

        expired_payload = {
            "sub": str(test_user.id),
            "type": TokenType.REFRESH.value,
            "iat": datetime.now(tz=timezone.utc) - timedelta(days=8),
            "exp": datetime.now(tz=timezone.utc) - timedelta(days=1),
        }
        expired_token = jwt.encode(
            expired_payload,
            config.jwt.secret,
            algorithm=config.jwt.algorithm,
        )

        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": f"Bearer {expired_token}"},
        )

        assert response.status_code == 401

    def test_refresh_wrong_token_type(self, client, access_token):
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 401

    def test_refresh_user_not_found(self, client):
        from arvo.config import config
        from arvo.services.auth import TokenType

        nonexistent_user_payload = {
            "sub": "99999",
            "type": TokenType.REFRESH.value,
            "iat": datetime.now(tz=timezone.utc),
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=7),
        }
        token = jwt.encode(
            nonexistent_user_payload,
            config.jwt.secret,
            algorithm=config.jwt.algorithm,
        )

        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 401

    def test_refresh_missing_bearer_prefix(self, client, refresh_token):
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": refresh_token},
        )

        assert response.status_code == 401

    def test_refresh_empty_authorization_header(self, client):
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": ""},
        )

        assert response.status_code == 401
