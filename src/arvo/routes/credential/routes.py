from flask import jsonify, g
from flask_pydantic.core import validate

from arvo.routes.credential import bp
from arvo.routes.credential.dto import (
    AWSCredentialCreateRequestDto,
    AWSCredentialCreateResponseDto,
)

from arvo.services.auth import TokenType
from arvo.services.credential import CredentialService

from arvo.middleware import authenticate


@bp.route("/", methods=["GET"])
@authenticate(TokenType.ACCESS)
def get_credentials():
    credentials = CredentialService.get_credentials_by_user(user=g.user)
    response = [
        {
            "id": cred.id,
            "name": cred.name,
            "type": cred.type.value,
        }
        for cred in credentials
    ]
    return jsonify(response), 200


@bp.route("/<int:credential_id>", methods=["DELETE"])
@authenticate(TokenType.ACCESS)
def delete_credential(credential_id: int):
    credential = CredentialService.delete_credential_by_id(g.user, credential_id)
    return jsonify(
        {
            "id": credential.id,
            "name": credential.name,
            "type": credential.type.value,
        }
    ), 200


@bp.route("/aws", methods=["POST"])
@authenticate(TokenType.ACCESS)
@validate()
def create_aws(body: AWSCredentialCreateRequestDto):
    credential = CredentialService.create_aws_credential(
        user=g.user,
        name=body.name,
        region=body.region,
        access_key_id=body.access_key_id,
        secret_access_key=body.secret_access_key,
    )

    response = AWSCredentialCreateResponseDto(
        id=credential.id,
        name=credential.name,
    )

    return jsonify(response.model_dump()), 201
