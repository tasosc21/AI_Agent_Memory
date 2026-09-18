from types import SimpleNamespace
from uuid import uuid4

from application.persistence_service import PersistenceService
from domain.context import Context
from domain.message import Message


class FakeUserRepository:

    def __init__(self):
        self.users = {}
        self.created_users = []

    def get(self, username):
        return self.users.get(username)

    def create(self, username):
        user = SimpleNamespace(
            user_id=uuid4(),
            username=username,
        )

        self.users[username] = user
        self.created_users.append(user)

        return user


class FakeConversationRepository:

    def __init__(self):
        self.created_conversations = []

    def create(self, user_id):
        conversation = SimpleNamespace(
            conversation_id=uuid4(),
            user_id=user_id,
        )

        self.created_conversations.append(conversation)

        return conversation


class FakeMessageRepository:

    def __init__(self):
        self.created_messages = []

    def create(self, message):
        self.created_messages.append(message)


def create_service():
    context = Context()
    user_repository = FakeUserRepository()
    conversation_repository = FakeConversationRepository()
    message_repository = FakeMessageRepository()

    service = PersistenceService(
        context,
        user_repository,
        conversation_repository,
        message_repository,
    )

    return (
        service,
        context,
        user_repository,
        conversation_repository,
        message_repository,
    )


def test_new_user_creates_user_and_conversation():
    (
        service,
        context,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service()

    message = Message(
        username="TestUser",
        role="user",
        content="Hello",
        conversation_id=None,
    )

    service.run(message)

    assert len(user_repository.created_users) == 1
    assert len(conversation_repository.created_conversations) == 1


def test_new_user_persists_message():
    (
        service,
        context,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service()

    message = Message(
        username="TestUser",
        role="user",
        content="Hello",
        conversation_id=None,
    )

    service.run(message)

    assert len(message_repository.created_messages) == 1
    assert message_repository.created_messages[0] is message


def test_new_user_assigns_conversation_id_to_message():
    (
        service,
        context,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service()

    message = Message(
        username="TestUser",
        role="user",
        content="Hello",
        conversation_id=None,
    )

    service.run(message)

    conversation = conversation_repository.created_conversations[0]

    assert message.conversation_id == conversation.conversation_id


def test_new_user_adds_conversation_to_context():
    (
        service,
        context,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service()

    message = Message(
        username="TestUser",
        role="user",
        content="Hello",
        conversation_id=None,
    )

    service.run(message)

    assert "testuser" in context.per_user


def test_new_user_adds_message_to_context_conversation():
    (
        service,
        context,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service()

    message = Message(
        username="TestUser",
        role="user",
        content="Hello",
        conversation_id=None,
    )

    service.run(message)

    conversation = context.per_user["testuser"]["conversation"]

    assert conversation.conversation == [
        {
            "role": "user",
            "content": "Hello",
        }
    ]


def test_existing_context_user_reuses_conversation():
    (
        service,
        context,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service()

    first_message = Message(
        username="TestUser",
        role="user",
        content="Hello",
        conversation_id=None,
    )

    service.run(first_message)

    first_conversation_id = first_message.conversation_id

    second_message = Message(
        username="TestUser",
        role="user",
        content="How are you?",
        conversation_id=None,
    )

    service.run(second_message)

    assert second_message.conversation_id == first_conversation_id
    assert len(conversation_repository.created_conversations) == 1


def test_existing_context_user_persists_second_message():
    (
        service,
        context,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service()

    first_message = Message(
        username="TestUser",
        role="user",
        content="Hello",
        conversation_id=None,
    )

    service.run(first_message)

    second_message = Message(
        username="TestUser",
        role="user",
        content="How are you?",
        conversation_id=None,
    )

    service.run(second_message)

    assert message_repository.created_messages == [
        first_message,
        second_message,
    ]


def test_current_context_contains_conversation_messages():
    (
        service,
        context,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service()

    first_message = Message(
        username="TestUser",
        role="user",
        content="Hello",
        conversation_id=None,
    )

    service.run(first_message)

    second_message = Message(
        username="TestUser",
        role="assistant",
        content="Hello! How can I help?",
        conversation_id=None,
    )

    service.run(second_message)

    assert context.current_context == [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hello! How can I help?",
        },
    ]