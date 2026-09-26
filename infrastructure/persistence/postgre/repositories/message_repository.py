from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.message import Message as DomainMessage
from infrastructure.persistence.postgre.models import Message as DBMessage


class MessageRepository:

    def get(self, session: Session, message_id: UUID) -> DBMessage | None:
        statement = select(DBMessage).where(DBMessage.message_id == message_id)
        return session.scalar(statement)

    def create(self, session: Session, message: DomainMessage) -> DBMessage:
        db_message = DBMessage(
            conversation_id=message.conversation_id,
            role=message.role.value,
            content=message.content,
        )

        session.add(db_message)
        session.flush()

        return db_message