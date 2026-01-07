from flask import Flask, Blueprint

from arvo.routes.auth import bp as auth_bp
from arvo.routes.credential import bp as credential_bp
from arvo.routes.deployment import bp as deployment_bp
from arvo.routes.user import bp as user_bp

bp = Blueprint("api", __name__)
bp.register_blueprint(auth_bp, url_prefix="/auth")
bp.register_blueprint(credential_bp, url_prefix="/credential")
bp.register_blueprint(deployment_bp, url_prefix="/deployment")
bp.register_blueprint(user_bp, url_prefix="/user")


def route(app: Flask):
    app.register_blueprint(bp, url_prefix="/api")
