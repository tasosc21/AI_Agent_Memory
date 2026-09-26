from sqlalchemy import select, update, func
from sqlalchemy.orm import Session

from infrastructure.persistence.postgre.models import User as DBUser
from domain.context import Context


class UserRepository:

    def create(self, session: Session, username: str) -> DBUser:
        user = DBUser(username=username.lower())
        session.add(user)
        session.flush()

        return user

    def get(self, session: Session, username: str) -> DBUser | None:
        statement = (
            select(DBUser)
            .where(DBUser.username == username.lower())
        )

        return session.scalar(statement)

    def update(self, session: Session, user: Context) -> None:
        statement = (
            update(DBUser)
            .where(DBUser.user_id == user.user_id)
            .values(
                summary=user.summary,
                profile=user.profile,
                last_interaction_at=func.now()
            )
        )
        session.execute(statement)
