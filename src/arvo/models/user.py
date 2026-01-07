from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from arvo.models.__base__ import Base

if TYPE_CHECKING:
    from arvo.models.credential import Credential
    from arvo.models.deployment import Deployment


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    credentials: Mapped[list["Credential"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    deployments: Mapped[list["Deployment"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
