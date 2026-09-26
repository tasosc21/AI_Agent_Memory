from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from infrastructure.persistence.postgre.models import (
    Conversation as DBConversation,
    Message as DBMessage,
)

from domain.context import Context


class ConversationRepository:

    def create(self, session: Session, user_id: UUID, meeting_id: UUID) -> DBConversation:
        conversation = DBConversation(user_id=user_id, meeting_id=meeting_id)
        session.add(conversation)
        session.flush()

        return conversation

    def get(self, session: Session, conversation_id: UUID) -> DBConversation:
        statement = (
            select(DBConversation)
            .where(DBConversation.conversation_id == conversation_id)
        )

        conversation = session.scalar(statement)

        if conversation is None:
            raise RuntimeError(
                f"Conversation {conversation_id} was not found in the database."
            )

        return conversation

    def get_messages(
        self,
        session: Session,
        conversation_id: UUID,
    ) -> Sequence:
        """
        Gets all messages of a conversation.
        """
        statement = (
            select(DBMessage.role, DBMessage.content)
            .where(DBMessage.conversation_id == conversation_id)
            .order_by(DBMessage.created_at)
        )

        return session.execute(statement).mappings().all()

    def update(self, session: Session, user: Context) -> None:
        statement = (
            update(DBConversation)
            .where(DBConversation.conversation_id == user.conversation_id)
            .values(
                summary=user.current_conversation_summary
                )
        )
        session.execute(statement)