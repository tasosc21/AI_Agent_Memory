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
from application.persistence_service import PersistenceService
from domain.context import Context


def test_conversation_persistence_workflow():
    context = Context()

    user_repository = UserRepository()
    conversation_repository = ConversationRepository()
    message_repository = MessageRepository()

    persistence_service = PersistenceService(
        context,
        user_repository,
        conversation_repository,
        message_repository,
    )

    # 1. User sends first message
    first_message = Message(
        username="TestUser",
        role="user",
        content="Hello, Agent",
        conversation_id=None,
    )

    persistence_service.run(first_message)

    # 2. A user and conversation should now exist
    user = user_repository.get("testuser")

    assert user is not None

    conversation_id = first_message.conversation_id

    assert conversation_id is not None

    # 3. User receives an assistant response
    second_message = Message(
        username="TestUser",
        role="assistant",
        content="Hello! How can I help?",
        conversation_id=None,
    )

    persistence_service.run(second_message)

    # 4. Both messages should belong to the same conversation
    assert second_message.conversation_id == conversation_id

    # 5. The conversation should contain both messages
    messages = conversation_repository.get(conversation_id)

    assert [message["role"] for message in messages] == [
        "user",
        "assistant",
    ]

    assert [message["content"] for message in messages] == [
        "Hello, Agent",
        "Hello! How can I help?",
    ]

    # 6. The in-memory context should also contain both messages
    assert context.current_context == [
        {"role": "user", "content": "Hello, Agent"},
        {"role": "assistant", "content": "Hello! How can I help?"},
    ]