from uuid import uuid4

from domain.conversation import Conversation
from domain.message import Message, MessageRole


def test_conversation_creation():
    conversation_id = uuid4()

    conversation = Conversation("Jane", conversation_id)

    assert conversation.username == "jane"
    assert conversation.id == conversation_id
    assert conversation.conversation == []


def test_add_message():
    conversation = Conversation("Jane", uuid4())

    message = Message(
        username="Jane",
        role=MessageRole.USER,
        content="Hello",
        conversation_id=conversation.id,
    )

    conversation.add(message)

    assert conversation.conversation == [
        {
            "role": "user",
            "content": "Hello",
        }
    ]