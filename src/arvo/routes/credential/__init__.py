from flask import Blueprint

bp = Blueprint("credential", __name__)

import arvo.routes.credential.routes  # noqa: F401, E402
