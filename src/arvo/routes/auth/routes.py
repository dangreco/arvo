from flask import jsonify, g
from flask_pydantic.core import validate
from werkzeug.exceptions import Unauthorized, BadRequest

from arvo.routes.auth import bp
from arvo.routes.auth.dto import SignupRequestDto, SignupResponseDto
from arvo.routes.auth.dto import LoginRequestDto, LoginResponseDto
from arvo.routes.auth.dto import RefreshResponseDto

from arvo.services.auth import AuthService, TokenType
from arvo.services.user import UserService

from arvo.middleware import authenticate


@bp.route("/signup", methods=["POST"])
@validate()
def signup(body: SignupRequestDto):
    try:
        user = UserService.create(body.email, body.password)
    except Exception as e:
        raise BadRequest(f"Error creating user: {str(e)}")

    response = SignupResponseDto(
        access=AuthService.create_token(user.id, TokenType.ACCESS),
        refresh=AuthService.create_token(user.id, TokenType.REFRESH),
    )
    return jsonify(response.model_dump()), 201


@bp.route("/login", methods=["POST"])
@validate()
def login(body: LoginRequestDto):
    user = UserService.get_by_email(body.email)
    if not user:
        raise Unauthorized("Invalid email")

    if not UserService.verify_password(user, body.password):
        raise Unauthorized("Invalid password")

    response = LoginResponseDto(
        access=AuthService.create_token(user.id, TokenType.ACCESS),
        refresh=AuthService.create_token(user.id, TokenType.REFRESH),
    )
    return jsonify(response.model_dump()), 200


@bp.route("/refresh", methods=["POST"])
@authenticate(TokenType.REFRESH)
@validate()
def refresh():
    response = RefreshResponseDto(
        access=AuthService.create_token(g.user.id, TokenType.ACCESS),
        refresh=AuthService.create_token(g.user.id, TokenType.REFRESH),
    )
    return jsonify(response.model_dump()), 200
