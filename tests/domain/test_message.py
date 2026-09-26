from uuid import uuid4

from domain.message import Message, MessageRole


def test_message_creation():
    conversation_id = uuid4()

    message = Message(
        username="TestUser",
        role=MessageRole.USER,
        content="Hello!",
        conversation_id=conversation_id,
    )

    assert message.username == "testuser"
    assert message.role == MessageRole.USER
    assert message.content == "Hello!"
    assert message.conversation_id == conversation_id


def test_username_is_lowercase():
    message = Message(
        username="JaNe",
        role=MessageRole.USER,
        content="Hello",
        conversation_id=None,
    )

    assert message.username == "jane"


def test_message_roles():
    assert MessageRole.USER.value == "user"
    assert MessageRole.ASSISTANT.value == "assistant"