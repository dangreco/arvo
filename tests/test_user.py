import json


class TestGetUser:
    def test_get_user_success(self, client, test_user, auth_headers):
        response = client.get("/user/", headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email

    def test_get_user_missing_token(self, client):
        response = client.get("/user/")

        assert response.status_code == 401

    def test_get_user_invalid_token(self, client):
        response = client.get(
            "/user/", headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401

    def test_get_user_expired_token(self, client, test_user):
        from arvo.services.auth import TokenType
        import jwt
        from datetime import datetime, timedelta, timezone

        expired_payload = {
            "sub": str(test_user.id),
            "type": TokenType.ACCESS.value,
            "iat": datetime.now(tz=timezone.utc) - timedelta(days=1),
            "exp": datetime.now(tz=timezone.utc) - timedelta(hours=1),
        }
        expired_token = jwt.encode(
            expired_payload, "your_secret_key", algorithm="HS256"
        )

        response = client.get(
            "/user/", headers={"Authorization": f"Bearer {expired_token}"}
        )

        assert response.status_code == 401

    def test_get_user_wrong_token_type(self, client, refresh_token):
        response = client.get(
            "/user/", headers={"Authorization": f"Bearer {refresh_token}"}
        )

        assert response.status_code == 401

    def test_get_user_malformed_auth_header(self, client, access_token):
        response = client.get("/user/", headers={"Authorization": access_token})

        assert response.status_code == 401
