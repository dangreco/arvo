from flask import jsonify, g
from flask_pydantic.core import validate

from arvo.routes.deployment import bp
from arvo.routes.deployment.dto import (
    DeploymentCreateRequestDto,
    DeploymentCreateResponseDto,
)

from arvo.services.auth import TokenType
from arvo.services.credential import CredentialService
from arvo.services.deployment import DeploymentService

from arvo.middleware import authenticate


@bp.route("/", methods=["POST"])
@authenticate(TokenType.ACCESS)
@validate()
def create(body: DeploymentCreateRequestDto):
    credential = CredentialService.get_credential_by_id(g.user, body.credential_id)
    deployment = DeploymentService.create(
        g.user,
        credential,
        body.prompt,
    )

    response = DeploymentCreateResponseDto(
        id=deployment.id,
        prompt=deployment.prompt,
        status=deployment.status,
        description=deployment.description,
        credential_id=deployment.credential_id,
    )

    return jsonify(response.model_dump()), 201


@bp.route("/", methods=["GET"])
@authenticate(TokenType.ACCESS)
@validate()
def list():
    deployments = DeploymentService.get_deployments_by_user(g.user)
    response = [
        {
            "id": deployment.id,
            "prompt": deployment.prompt,
            "status": deployment.status,
            "description": deployment.description,
            "credential_id": deployment.credential_id,
        }
        for deployment in deployments
    ]
    return jsonify(response), 200


@bp.route("/<int:id>", methods=["GET"])
@authenticate(TokenType.ACCESS)
@validate()
def get(id: int):
    deployment = DeploymentService.get_deployment_by_id(
        g.user,
        id,
    )

    response = DeploymentCreateResponseDto(
        id=deployment.id,
        prompt=deployment.prompt,
        status=deployment.status,
        description=deployment.description,
        credential_id=deployment.credential_id,
    )

    return jsonify(response.model_dump()), 200
