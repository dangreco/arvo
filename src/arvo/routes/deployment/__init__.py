from flask import Blueprint

bp = Blueprint("deployment", __name__)

import arvo.routes.deployment.routes  # noqa: F401, E402
