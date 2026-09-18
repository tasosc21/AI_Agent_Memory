from sqlalchemy import select

from infrastructure.persistence.postgre.database import SessionFactory
from infrastructure.persistence.postgre.models import User


class UserRepository:

    def __init__(self) -> None:
        self.session_factory = SessionFactory

    def create(self, username: str) -> User:
        with self.session_factory() as session:
            user = User(username=username.lower())
            session.add(user)
            session.commit()
            session.refresh(user)

            return user

    def get(self, username: str) -> User | None:
        with self.session_factory() as session:
            statement = (
                select(User)
                .where(User.username == username)
            )

            return session.scalar(statement)