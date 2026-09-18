from domain.message import Message


def test_message():
    message = Message(
        username="TestUser",
        role="user",
        content="Hello, Assistant",
        conversation_id=None,
    )

    assert message.content == "Hello, Assistant"
    assert message.role == "user"
    assert message.username == "testuser"
    assert message.conversation_id is None