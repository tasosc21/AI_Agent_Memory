from uuid import uuid4

import pytest

from infrastructure.persistence.postgre.models import (
    Conversation as DBConversation,
    Meeting as DBMeeting,
    Message as DBMessage,
    User as DBUser,
)
from infrastructure.persistence.postgre.repositories.conversation_repository import (
    ConversationRepository,
)


def test_create_conversation(session):
    user = DBUser(username="jane")
    meeting = DBMeeting()

    session.add_all([user, meeting])
    session.flush()

    print("USER ID:", user.user_id)
    print("MEETING ID:", meeting.meeting_id)
    print("USER FROM SESSION:", session.get(DBUser, user.user_id))
    print("MEETING FROM SESSION:", session.get(DBMeeting, meeting.meeting_id))

    repository = ConversationRepository()

    conversation = repository.create(
        session,
        user.user_id,
        meeting.meeting_id,
    )

    assert isinstance(conversation, DBConversation)
    assert conversation.conversation_id is not None
    assert conversation.user_id == user.user_id
    assert conversation.meeting_id == meeting.meeting_id


def test_get_existing_conversation(session):
    repository = ConversationRepository()

    user = DBUser(username="jane")
    meeting = DBMeeting()

    session.add_all([user, meeting])
    session.flush()

    conversation = repository.create(
        session,
        user.user_id,
        meeting.meeting_id,
    )

    result = repository.get(
        session,
        conversation.conversation_id,
    )

    assert result.conversation_id == conversation.conversation_id
    assert result.user_id == user.user_id
    assert result.meeting_id == meeting.meeting_id


def test_get_nonexistent_conversation(session):
    repository = ConversationRepository()

    with pytest.raises(
        RuntimeError,
        match="was not found in the database",
    ):
        repository.get(
            session,
            uuid4(),
        )


def test_get_messages(session):
    repository = ConversationRepository()

    user = DBUser(username="jane")
    meeting = DBMeeting()

    session.add_all([user, meeting])
    session.flush()

    conversation = repository.create(
        session,
        user.user_id,
        meeting.meeting_id,
    )

    session.add_all(
        [
            DBMessage(
                conversation_id=conversation.conversation_id,
                role="user",
                content="Hello",
            ),
            DBMessage(
                conversation_id=conversation.conversation_id,
                role="assistant",
                content="Hello! How can I help?",
            ),
        ]
    )

    session.flush()

    messages = repository.get_messages(
        session,
        conversation.conversation_id,
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello"
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "Hello! How can I help?"