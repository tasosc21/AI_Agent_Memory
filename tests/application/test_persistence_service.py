from uuid import uuid4

from application.context_store import ContextStore
from application.persistence_service import PersistenceService
from domain.context import Context
from domain.message import Message, MessageRole

from tests.fakes import (
    FakeContextStore,
    FakeConversationRepository,
    FakeMessageRepository,
    FakeMeetingRepository,
    FakeSessionFactory,
    FakeUserRepository,
)


def create_service(monkeypatch):
    monkeypatch.setattr(
        "application.persistence_service.SessionFactory",
        FakeSessionFactory(),
    )

    context_store = FakeContextStore()
    user_repository = FakeUserRepository()
    conversation_repository = FakeConversationRepository()
    message_repository = FakeMessageRepository()
    meeting_repository = FakeMeetingRepository()

    service = PersistenceService(
        context_store,
        user_repository,
        conversation_repository,
        meeting_repository,
        message_repository,
    )

    return (
        service,
        context_store,
        user_repository,
        conversation_repository,
        message_repository,
    )


def test_new_user_creates_user_conversation_and_message(monkeypatch):
    (
        service,
        context_store,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service(monkeypatch)

    message = Message(
        username="TestUser",
        role=MessageRole.USER,
        content="Hello",
        conversation_id=None,
    )

    result = service.run(message)

    assert len(user_repository.created_users) == 1
    assert len(conversation_repository.created_conversations) == 1
    assert len(message_repository.created_messages) == 1
    assert result["message"].role == MessageRole.USER


def test_new_user_assigns_conversation_id_to_message(monkeypatch):
    (
        service,
        context_store,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service(monkeypatch)

    message = Message(
        username="TestUser",
        role=MessageRole.USER,
        content="Hello",
        conversation_id=None,
    )

    result = service.run(message)

    conversation_id = (
        conversation_repository.created_conversations[0].conversation_id
    )

    assert message.conversation_id == conversation_id
    assert result["conversation"].id == conversation_id


def test_new_conversation_belongs_to_current_meeting(monkeypatch):
    (
        service,
        context_store,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service(monkeypatch)

    message = Message(
        username="TestUser",
        role=MessageRole.USER,
        content="Hello",
        conversation_id=None,
    )

    service.run(message)

    conversation = conversation_repository.created_conversations[0]

    assert conversation.meeting_id == service.meeting_id


def test_cached_user_reuses_conversation(monkeypatch):
    (
        service,
        context_store,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service(monkeypatch)

    conversation_id = uuid4()
    user_id = uuid4()

    user = Context(
        user_id=user_id,
        conversation_id=conversation_id,
        profile="",
        summary="",
    )

    context_store.context_cache["testuser"] = user

    user_repository.users["testuser"] = type(
        "FakeUser",
        (),
        {
            "user_id": user_id,
            "username": "testuser",
            "profile": "",
            "summary": "",
        },
    )()

    message = Message(
        username="TestUser",
        role=MessageRole.USER,
        content="Hello again",
        conversation_id=None,
    )

    service.run(message)

    assert message.conversation_id == conversation_id
    assert len(conversation_repository.created_conversations) == 0


def test_db_message_role_is_converted_to_domain_role(monkeypatch):
    (
        service,
        context_store,
        user_repository,
        conversation_repository,
        message_repository,
    ) = create_service(monkeypatch)

    message = Message(
        username="TestUser",
        role=MessageRole.ASSISTANT,
        content="Hello!",
        conversation_id=None,
    )

    result = service.run(message)

    assert result["message"].role == MessageRole.ASSISTANT