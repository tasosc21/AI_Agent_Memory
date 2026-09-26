from uuid import uuid4

from application.context_service import ContextService
from application.types import PersistenceResult
from domain.message import Message as DomainMessage, MessageRole
from domain.conversation import Conversation as DomainConversation
from domain.user import User as DomainUser

from tests.fakes import FakeContextStore, FakePromptRepository


def create_service():
    context_store = FakeContextStore()
    prompt_repository = FakePromptRepository()

    service = ContextService(
        context_store,
        prompt_repository,
    )

    return service, context_store


def create_domain_objects(username="Jane") -> PersistenceResult:
    user = DomainUser(
        id=uuid4(),
        username=username,
        profile="",
        summary="User summary",
    )

    conversation = DomainConversation(
        username=username,
        conversation_id=uuid4(),
    )

    message = DomainMessage(
        username=username,
        role=MessageRole.USER,
        content="Hello",
        conversation_id=conversation.id,
    )

    return {
        "user": user,
        "conversation": conversation,
        "message": message,
    }


def test_new_user_is_added_to_context():
    service, context_store = create_service()
    domain_objects = create_domain_objects()

    service.run(domain_objects)

    assert "jane" in context_store.context_cache


def test_existing_user_context_is_reused():
    service, context_store = create_service()
    domain_objects = create_domain_objects()

    service.run(domain_objects)

    first_context = context_store.context_cache["jane"]

    service.run(domain_objects)

    second_context = context_store.context_cache["jane"]

    assert second_context is first_context
    assert len(second_context.messages) == 2


def test_run_returns_full_context():
    service, context_store = create_service()
    domain_objects = create_domain_objects()

    result = service.run(domain_objects)

    assert result["username"] == "jane"
    assert result["user_summary"] == "User summary"
    assert result["conversation_summary"] == ""
    assert result["messages"] == [
        {
            "role": "user",
            "content": "Hello",
        }
    ]
    assert result["system"] == "System prompt"
    assert result["developer"] == "Developer prompt"