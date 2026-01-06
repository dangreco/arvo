from functools import wraps
from flask import request, g
from werkzeug.exceptions import Unauthorized

from arvo.services.auth import AuthService, TokenType
from arvo.services.user import UserService


def authenticate(type_: TokenType):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                raise Unauthorized("Missing token")

            token = str(token)
            if not token.startswith("Bearer "):
                raise Unauthorized("Missing token")

            try:
                token = token.replace("Bearer ", "")
                payload = AuthService.verify_token(token, type_)
                user_id = int(payload["sub"])
            except Exception as e:
                raise Unauthorized(f"Error: {str(e)}")

            user = UserService.get_by_id(user_id)
            if not user:
                raise Unauthorized("User not found")

            g.user = user
            return f(*args, **kwargs)

        return wrapper

    return decorator
