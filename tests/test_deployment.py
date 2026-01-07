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


@pytest.fixture
def test_deployment(test_user, test_aws_credential, db):
    from arvo.services.deployment import DeploymentService

    deployment = DeploymentService.create(
        user=test_user,
        credential=test_aws_credential,
        prompt="Deploy a simple web server",
    )
    return deployment


class TestCreateDeployment:
    def test_create_deployment_success(self, client, auth_headers, test_aws_credential):
        from arvo.models.deployment import DeploymentStatus

        response = client.post(
            "/api/deployment/",
            headers=auth_headers,
            json={
                "credential_id": test_aws_credential.id,
                "prompt": "Deploy a simple web server",
            },
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert "id" in data
        assert data["prompt"] == "Deploy a simple web server"
        assert data["status"] == DeploymentStatus.PENDING.value
        assert data["credential_id"] == test_aws_credential.id
        assert data["description"] is None

    def test_create_deployment_missing_token(self, client, test_aws_credential):
        response = client.post(
            "/api/deployment/",
            json={
                "credential_id": test_aws_credential.id,
                "prompt": "Deploy a simple web server",
            },
        )

        assert response.status_code == 401

    def test_create_deployment_invalid_token(self, client, test_aws_credential):
        response = client.post(
            "/api/deployment/",
            headers={"Authorization": "Bearer invalid_token"},
            json={
                "credential_id": test_aws_credential.id,
                "prompt": "Deploy a simple web server",
            },
        )

        assert response.status_code == 401

    def test_create_deployment_missing_credential_id(self, client, auth_headers):
        response = client.post(
            "/api/deployment/",
            headers=auth_headers,
            json={
                "prompt": "Deploy a simple web server",
            },
        )

        assert response.status_code == 400

    def test_create_deployment_missing_prompt(
        self, client, auth_headers, test_aws_credential
    ):
        response = client.post(
            "/api/deployment/",
            headers=auth_headers,
            json={
                "credential_id": test_aws_credential.id,
            },
        )

        assert response.status_code == 400

    def test_create_deployment_invalid_credential_id(self, client, auth_headers):
        with pytest.raises(ValueError):
            client.post(
                "/api/deployment/",
                headers=auth_headers,
                json={
                    "credential_id": 999,
                    "prompt": "Deploy a simple web server",
                },
            )

    def test_create_deployment_wrong_user_credential(
        self, client, db, test_aws_credential
    ):
        from arvo.services.user import UserService
        from arvo.services.auth import AuthService, TokenType

        other_user = UserService.create("other@example.com", "password123")
        other_token = AuthService.create_token(other_user.id, TokenType.ACCESS)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        with pytest.raises(ValueError):
            client.post(
                "/api/deployment/",
                headers=other_headers,
                json={
                    "credential_id": test_aws_credential.id,
                    "prompt": "Deploy a simple web server",
                },
            )


class TestListDeployments:
    def test_list_deployments_empty(self, client, auth_headers):
        response = client.get("/api/deployment/", headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_list_deployments_with_data(self, client, auth_headers, test_deployment):
        response = client.get("/api/deployment/", headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["id"] == test_deployment.id
        assert data[0]["prompt"] == test_deployment.prompt
        assert data[0]["status"] == test_deployment.status
        assert data[0]["credential_id"] == test_deployment.credential_id

    def test_list_deployments_multiple(
        self, client, auth_headers, test_aws_credential, db
    ):
        from arvo.services.deployment import DeploymentService
        from arvo.services.user import UserService

        user = UserService.get_by_email("test@example.com")
        if not user:
            raise Exception("User not found")

        deployment1 = DeploymentService.create(
            user=user,
            credential=test_aws_credential,
            prompt="Deploy web server",
        )
        deployment2 = DeploymentService.create(
            user=user,
            credential=test_aws_credential,
            prompt="Deploy database",
        )

        response = client.get("/api/deployment/", headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]["id"] == deployment1.id
        assert data[1]["id"] == deployment2.id

    def test_list_deployments_missing_token(self, client):
        response = client.get("/api/deployment/")

        assert response.status_code == 401

    def test_list_deployments_invalid_token(self, client):
        response = client.get(
            "/api/deployment/", headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401

    def test_list_deployments_only_shows_user_deployments(
        self, client, auth_headers, db, test_deployment
    ):
        from arvo.services.user import UserService
        from arvo.services.credential import CredentialService
        from arvo.services.deployment import DeploymentService

        other_user = UserService.create("other@example.com", "password123")
        other_credential = CredentialService.create_aws_credential(
            user=other_user,
            name="Other AWS Credential",
            region="us-west-2",
            access_key_id="AKIAIOSFODNN7EXAMPLE",
            secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        )
        other_deployment = DeploymentService.create(
            user=other_user,
            credential=other_credential,
            prompt="Other user deployment",
        )

        response = client.get("/api/deployment/", headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["id"] == test_deployment.id
        assert data[0]["id"] != other_deployment.id


class TestGetDeployment:
    def test_get_deployment_success(self, client, auth_headers, test_deployment):
        response = client.get(
            f"/api/deployment/{test_deployment.id}", headers=auth_headers
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == test_deployment.id
        assert data["prompt"] == test_deployment.prompt
        assert data["status"] == test_deployment.status
        assert data["credential_id"] == test_deployment.credential_id
        assert data["description"] == test_deployment.description

    def test_get_deployment_missing_token(self, client, test_deployment):
        response = client.get(f"/api/deployment/{test_deployment.id}")

        assert response.status_code == 401

    def test_get_deployment_invalid_token(self, client, test_deployment):
        response = client.get(
            f"/api/deployment/{test_deployment.id}",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401

    def test_get_deployment_not_found(self, client, auth_headers):
        with pytest.raises(ValueError):
            client.get("/api/deployment/999", headers=auth_headers)

    def test_get_deployment_wrong_user(self, client, db, test_deployment):
        from arvo.services.user import UserService
        from arvo.services.auth import AuthService, TokenType

        other_user = UserService.create("other@example.com", "password123")
        other_token = AuthService.create_token(other_user.id, TokenType.ACCESS)
        other_headers = {"Authorization": f"Bearer {other_token}"}

        with pytest.raises(ValueError):
            client.get(f"/api/deployment/{test_deployment.id}", headers=other_headers)
