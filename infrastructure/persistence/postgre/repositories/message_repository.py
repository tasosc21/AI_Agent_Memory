from uuid import UUID

from sqlalchemy import select

from domain.message import Message as DomainMessage
from infrastructure.persistence.postgre.database import SessionFactory
from infrastructure.persistence.postgre.models import Message


class MessageRepository:

    def __init__(self) -> None:
        self.session_factory = SessionFactory

    def get(self, message_id: UUID) -> Message | None:
        with self.session_factory() as session:
            statement = select(Message).where(Message.message_id == message_id)
            return session.scalar(statement)

    def create(self, message: DomainMessage) -> Message:
        with self.session_factory() as session:
            db_message = Message(
                conversation_id=message.conversation_id,
                role=message.role,
                content=message.content,
            )

            session.add(db_message)
            session.commit()
            session.refresh(db_message)

            return db_message