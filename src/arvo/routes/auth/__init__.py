from flask import Blueprint

bp = Blueprint("auth", __name__)

import arvo.routes.auth.routes  # noqa: F401, E402
