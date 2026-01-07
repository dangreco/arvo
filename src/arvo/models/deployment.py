from typing import TYPE_CHECKING
from enum import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from arvo.models.__base__ import Base

if TYPE_CHECKING:
    from arvo.models.user import User
    from arvo.models.credential import Credential


class DeploymentStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PLANNING = "planning"
    APPLYING = "applying"
    ACTIVE = "active"
    FAILED = "failed"


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[int] = mapped_column(primary_key=True)
    prompt: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    status_message: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="deployments")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    credential: Mapped["Credential"] = relationship(back_populates="deployments")
    credential_id: Mapped[int] = mapped_column(
        ForeignKey("credentials.id"),
        nullable=False,
    )
