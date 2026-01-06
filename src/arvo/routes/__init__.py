from flask import Flask

from arvo.routes.auth import bp as auth_bp
from arvo.routes.credential import bp as credential_bp
from arvo.routes.user import bp as user_bp


def route(app: Flask):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(credential_bp, url_prefix="/credential")
    app.register_blueprint(user_bp, url_prefix="/user")
