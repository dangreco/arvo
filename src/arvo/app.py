from flask import Flask
from flask_cors import CORS

from arvo.routes import route

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
CORS(app)

route(app)
