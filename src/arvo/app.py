from pathlib import Path
from flask import Flask, send_from_directory
from flask_cors import CORS

from arvo.routes import route

app = Flask(
    __name__,
    static_folder=(Path(__file__).parent.parent.parent / "frontend" / "dist"),
    static_url_path="",
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
CORS(app)

# REST routes
route(app)


@app.route("/")
def serve_index():
    return send_from_directory(str(app.static_folder), "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(str(app.static_folder), path)
