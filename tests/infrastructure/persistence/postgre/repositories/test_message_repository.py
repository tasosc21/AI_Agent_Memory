from uuid import uuid4

from domain.message import Message, MessageRole
from infrastructure.persistence.postgre.models import (
    Conversation as DBConversation,
    Message as DBMessage,
    Meeting as DBMeeting,
    User as DBUser,
)
from infrastructure.persistence.postgre.repositories.message_repository import (
    MessageRepository,
)


def test_create_message(session):
    repository = MessageRepository()

    user = DBUser(username="jane")
    meeting = DBMeeting()

    session.add_all([user, meeting])
    session.flush()

    conversation = DBConversation(
        user_id=user.user_id,
        meeting_id=meeting.meeting_id,
    )

    session.add(conversation)
    session.flush()

    message = Message(
        "Jane",
        MessageRole.USER,
        "Hello",
        conversation.conversation_id,
    )

    db_message = repository.create(
        session,
        message,
    )

    assert isinstance(db_message, DBMessage)
    assert db_message.message_id is not None
    assert db_message.conversation_id == conversation.conversation_id
    assert db_message.role == "user"
    assert db_message.content == "Hello"


def test_get_existing_message(session):
    repository = MessageRepository()

    user = DBUser(username="jane")
    meeting = DBMeeting()

    session.add_all([user, meeting])
    session.flush()

    conversation = DBConversation(
        user_id=user.user_id,
        meeting_id=meeting.meeting_id,
    )

    session.add(conversation)
    session.flush()

    message = Message(
        "Jane",
        MessageRole.ASSISTANT,
        "Hello!",
        conversation.conversation_id,
    )

    created = repository.create(
        session,
        message,
    )

    result = repository.get(
        session,
        created.message_id,
    )

    assert result is not None
    assert result.message_id == created.message_id
    assert result.role == "assistant"
    assert result.content == "Hello!"


def test_get_nonexistent_message(session):
    repository = MessageRepository()

    result = repository.get(
        session,
        uuid4(),
    )

    assert result is None