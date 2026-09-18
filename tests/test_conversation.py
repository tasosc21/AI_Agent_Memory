from uuid import uuid4

from domain.conversation import Conversation
from domain.message import Message


def test_conversation_starts_empty():
    conversation_id = uuid4()

    conversation = Conversation(
        username="testuser",
        conversation_id=conversation_id,
    )

    assert conversation.conversation == []


def test_conversation_stores_username():
    conversation_id = uuid4()

    conversation = Conversation(
        username="testuser",
        conversation_id=conversation_id,
    )

    assert conversation.username == "testuser"


def test_conversation_stores_conversation_id():
    conversation_id = uuid4()

    conversation = Conversation(
        username="testuser",
        conversation_id=conversation_id,
    )

    assert conversation.conversation_id == conversation_id


def test_add_message():
    conversation_id = uuid4()

    conversation = Conversation(
        username="testuser",
        conversation_id=conversation_id,
    )

    message = Message(
        username="testuser",
        role="user",
        content="Hello, Agent",
        conversation_id=conversation_id,
    )

    conversation.add(message)

    assert conversation.conversation == [
        {
            "role": "user",
            "content": "Hello, Agent",
        }
    ]


def test_add_multiple_messages_preserves_order():
    conversation_id = uuid4()

    conversation = Conversation(
        username="testuser",
        conversation_id=conversation_id,
    )

    first_message = Message(
        username="testuser",
        role="user",
        content="First",
        conversation_id=conversation_id,
    )

    second_message = Message(
        username="testuser",
        role="assistant",
        content="Second",
        conversation_id=conversation_id,
    )

    conversation.add(first_message)
    conversation.add(second_message)

    assert conversation.conversation == [
        {
            "role": "user",
            "content": "First",
        },
        {
            "role": "assistant",
            "content": "Second",
        },
    ]