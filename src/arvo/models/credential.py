from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

from arvo.models.__base__ import Base

if TYPE_CHECKING:
    from arvo.models.user import User


class CredentialType(Enum):
    AWS = "aws"


class Credential(Base):
    __tablename__ = "credentials"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    type: Mapped[CredentialType] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="credentials")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": None,
    }


class AWSCredential(Credential):
    __tablename__ = "credentials_aws"

    id: Mapped[int] = mapped_column(ForeignKey("credentials.id"), primary_key=True)
    region: Mapped[str] = mapped_column()
    access_key_id: Mapped[str] = mapped_column()
    secret_access_key: Mapped[str] = mapped_column()

    __mapper_args__ = {
        "polymorphic_identity": CredentialType.AWS,
    }
