from flask import jsonify, g
from flask_pydantic.core import validate

from arvo.routes.user import bp
from arvo.routes.user.dto import GetUserResponseDto

from arvo.services.auth import TokenType

from arvo.middleware import authenticate


@bp.route("/", methods=["GET"])
@authenticate(TokenType.ACCESS)
@validate()
def get_user():
    response = GetUserResponseDto(
        id=g.user.id,
        email=g.user.email,
    )
    return jsonify(response.model_dump()), 200
