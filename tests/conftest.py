import pytest
from flask import Flask
from flask_cors import CORS
from arvo.providers.database import db as _db
from arvo.routes import route
from arvo.services.auth import AuthService, TokenType


@pytest.fixture(scope="function")
def app():
    test_app = Flask(__name__)
    test_app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    CORS(test_app)
    route(test_app)
    _db.init_app(test_app)

    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        yield _db


@pytest.fixture
def test_user(db):
    from arvo.services.user import UserService

    user = UserService.create("test@example.com", "password123")
    return user


@pytest.fixture
def access_token(test_user):
    return AuthService.create_token(test_user.id, TokenType.ACCESS)


@pytest.fixture
def refresh_token(test_user):
    return AuthService.create_token(test_user.id, TokenType.REFRESH)


@pytest.fixture
def auth_headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}
