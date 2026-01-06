from flask import Blueprint

bp = Blueprint("user", __name__)

import arvo.routes.user.routes  # noqa: F401, E402
