from flask_sqlalchemy import SQLAlchemy

from arvo.models.__base__ import Base

from arvo.models.user import User  # noqa: F401
from arvo.models.credential import Credential  # noqa: F401
from arvo.models.deployment import Deployment  # noqa: F401

db = SQLAlchemy(model_class=Base)
