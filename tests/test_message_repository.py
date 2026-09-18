from infrastructure.persistence.postgre.repositories.conversation_repository import (
    ConversationRepository,
)
from infrastructure.persistence.postgre.repositories.message_repository import (
    MessageRepository,
)
from infrastructure.persistence.postgre.repositories.user_repository import (
    UserRepository,
)
from domain.message import Message
from uuid import UUID

import pytest
from sqlalchemy.exc import IntegrityError


def create_conversation():
    user_repository = UserRepository()
    conversation_repository = ConversationRepository()

    user = user_repository.create("TestUser")

    return conversation_repository.create(user.user_id)


def test_create():
    conversation = create_conversation()
    repository = MessageRepository()

    message = Message(
        username="TestUser",
        role="user",
        content="Hello, Agent",
        conversation_id=conversation.conversation_id,
    )

    db_message = repository.create(message)

    assert db_message.message_id is not None
    assert db_message.conversation_id == conversation.conversation_id
    assert db_message.role == "user"
    assert db_message.content == "Hello, Agent"


def test_message_belongs_to_correct_conversation():
    conversation = create_conversation()
    repository = MessageRepository()

    message = Message(
        username="TestUser",
        role="user",
        content="Hello, Agent",
        conversation_id=conversation.conversation_id,
    )

    db_message = repository.create(message)

    assert db_message.conversation_id == conversation.conversation_id


def test_get():
    conversation = create_conversation()
    repository = MessageRepository()

    message = Message(
        username="TestUser",
        role="user",
        content="Hello, Agent",
        conversation_id=conversation.conversation_id,
    )

    created_message = repository.create(message)

    retrieved_message = repository.get(created_message.message_id)

    assert retrieved_message is not None
    assert retrieved_message.message_id == created_message.message_id
    assert retrieved_message.content == "Hello, Agent"

def test_cannot_create_message_for_nonexistent_conversation():
    repository = MessageRepository()

    message = Message(
        username="TestUser",
        role="user",
        content="This should fail",
        conversation_id=UUID(
            "00000000-0000-0000-0000-000000000000"
        ),
    )

    with pytest.raises(IntegrityError):
        repository.create(message)