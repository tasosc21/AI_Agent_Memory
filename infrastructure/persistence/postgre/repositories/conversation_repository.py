from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select

from infrastructure.persistence.postgre.database import SessionFactory
from infrastructure.persistence.postgre.models import Conversation, Message


class ConversationRepository:

    def __init__(self) -> None:
        self.session_factory = SessionFactory

    def create(self, user_id: UUID) -> Conversation:
        with self.session_factory() as session:
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

            return conversation

    def get(self, conversation_id: UUID) -> Sequence:
        """
        Gets all messages of a conversation.
        """
        with self.session_factory() as session:
            statement = (
                select(Message.role, Message.content)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at)
            )
            return session.execute(statement).mappings().all()