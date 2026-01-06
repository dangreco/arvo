from arvo.app import app
from arvo.providers.database import db


def main() -> None:
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(host="127.0.0.1", port=5000)
