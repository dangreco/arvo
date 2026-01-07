from arvo.providers.database import db

from arvo.models.user import User
from arvo.models.credential import Credential, AWSCredential


class CredentialService:
    @staticmethod
    def get_credentials_by_user(user: User) -> list[Credential]:
        return user.credentials

    @staticmethod
    def get_credential_by_id(user: User, id: int) -> Credential:
        credential = (
            db.session.query(Credential)
            .filter_by(id=id)
            .filter_by(user_id=user.id)
            .first()
        )

        if not credential:
            raise ValueError("Credential not found")

        return credential

    @staticmethod
    def delete_credential_by_id(user: User, id: int) -> Credential:
        credential = CredentialService.get_credential_by_id(user, id)

        db.session.delete(credential)
        db.session.commit()

        return credential

    @staticmethod
    def create_aws_credential(
        user: User,
        name: str,
        region: str,
        access_key_id: str,
        secret_access_key: str,
    ) -> AWSCredential:
        credential = AWSCredential(
            name=name,
            region=region,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
        )

        user.credentials.append(credential)

        db.session.commit()
        db.session.refresh(credential)

        return credential
