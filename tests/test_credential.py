import json
import pytest


@pytest.fixture
def test_aws_credential(test_user, db):
    from arvo.services.credential import CredentialService

    credential = CredentialService.create_aws_credential(
        user=test_user,
        name="Test AWS Credential",
        region="us-east-1",
        access_key_id="AKIAIOSFODNN7EXAMPLE",
        secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    )
    return credential


class TestGetCredentials:
    def test_get_credentials_empty(self, client, auth_headers):
        response = client.get("/api/credential/", headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_get_credentials_with_data(self, client, auth_headers, test_aws_credential):
        response = client.get("/api/credential/", headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["id"] == test_aws_credential.id
        assert data[0]["name"] == test_aws_credential.name
        assert data[0]["type"] == "aws"

    def test_get_credentials_missing_token(self, client):
        response = client.get("/api/credential/")

        assert response.status_code == 401

    def test_get_credentials_invalid_token(self, client):
        response = client.get(
            "/api/credential/", headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401


class TestCreateAWSCredential:
    def test_create_aws_credential_success(self, client, auth_headers):
        response = client.post(
            "/api/credential/aws",
            headers=auth_headers,
            json={
                "name": "My AWS Account",
                "region": "us-west-2",
                "access_key_id": "AKIAIOSFODNN7EXAMPLE",
                "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            },
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert "id" in data
        assert data["name"] == "My AWS Account"

    def test_create_aws_credential_missing_token(self, client):
        response = client.post(
            "/api/credential/aws",
            json={
                "name": "My AWS Account",
                "region": "us-west-2",
                "access_key_id": "AKIAIOSFODNN7EXAMPLE",
                "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            },
        )

        assert response.status_code == 401

    def test_create_aws_credential_missing_fields(self, client, auth_headers):
        response = client.post(
            "/api/credential/aws",
            headers=auth_headers,
            json={"name": "My AWS Account"},
        )

        assert response.status_code == 400

    def test_create_aws_credential_invalid_token(self, client):
        response = client.post(
            "/api/credential/aws",
            headers={"Authorization": "Bearer invalid_token"},
            json={
                "name": "My AWS Account",
                "region": "us-west-2",
                "access_key_id": "AKIAIOSFODNN7EXAMPLE",
                "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            },
        )

        assert response.status_code == 401


class TestDeleteCredential:
    def test_delete_credential_success(self, client, auth_headers, test_aws_credential):
        response = client.delete(
            f"/api/credential/{test_aws_credential.id}", headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == test_aws_credential.id
        assert data["name"] == test_aws_credential.name
        assert data["type"] == "aws"

        get_response = client.get("/api/credential/", headers=auth_headers)
        get_data = json.loads(get_response.data)
        assert len(get_data) == 0

    def test_delete_credential_not_found(self, client, auth_headers):
        # Service raises ValueError when credential not found, which Flask converts to 500
        with pytest.raises(ValueError):
            client.delete("/api/credential/999", headers=auth_headers)

    def test_delete_credential_missing_token(self, client, test_aws_credential):
        response = client.delete(f"/api/credential/{test_aws_credential.id}")

        assert response.status_code == 401

    def test_delete_credential_invalid_token(self, client, test_aws_credential):
        response = client.delete(
            f"/api/credential/{test_aws_credential.id}",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401

    def test_delete_credential_wrong_user(self, client, db, test_aws_credential):
        from arvo.services.user import UserService
        from arvo.services.auth import AuthService, TokenType

        other_user = UserService.create("other@example.com", "password123")
        other_token = AuthService.create_token(other_user.id, TokenType.ACCESS)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        # Service raises ValueError when credential belongs to another user
        with pytest.raises(ValueError):
            client.delete(
                f"/api/credential/{test_aws_credential.id}", headers=other_headers
            )
