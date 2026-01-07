from arvo.providers.database import db

from arvo.models.deployment import Deployment, DeploymentStatus
from arvo.models.credential import Credential
from arvo.models.user import User


class DeploymentService:
    @staticmethod
    def create(
        user: User,
        credential: Credential,
        prompt: str,
    ) -> Deployment:
        deployment = Deployment(
            user=user,
            credential=credential,
            prompt=prompt,
            status=DeploymentStatus.PENDING.value,
        )

        db.session.add(deployment)
        db.session.commit()
        db.session.refresh(deployment)

        # TODO: Add to job queue

        return deployment

    @staticmethod
    def get_deployments_by_user(user: User) -> list[Deployment]:
        return user.deployments

    @staticmethod
    def get_deployment_by_id(user: User, id: int) -> Deployment:
        deployment = (
            db.session.query(Deployment)
            .filter_by(id=id)
            .filter_by(user_id=user.id)
            .first()
        )

        if not deployment:
            raise ValueError("Deployment not found")

        return deployment
