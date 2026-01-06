from argon2 import PasswordHasher

from arvo.providers.database import db
from arvo.models.user import User


class UserService:
    @staticmethod
    def create(email: str, password: str) -> User:
        user = User(
            email=email,
            password=PasswordHasher().hash(password),
        )

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        return user

    @staticmethod
    def verify_password(user: User, password: str) -> bool:
        try:
            PasswordHasher().verify(user.password, password)
            return True
        except Exception:
            return False

    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        return db.session.query(User).filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return db.session.query(User).filter_by(email=email).first()
