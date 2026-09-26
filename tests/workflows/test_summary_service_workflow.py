from unittest.mock import Mock
from uuid import uuid4

from application.summary_service import SummaryService
from domain.context import Context
from domain.message import Message, MessageRole
from tests.fakes import FakeContextStore, FakePromptRepository


def create_service():
    llm = Mock()

    llm.summarise_user_current_conversation.return_value = (
        "User conversation summary."
    )

    llm.summarise_all_users_current_conversation.return_value = (
        "Overall conversation summary."
    )

    context_store = FakeContextStore()

    context_store.context_cache["jane"] = Context(
        user_id=uuid4(),
        profile="",
        summary="",
        conversation_id=uuid4(),
    )

    service = SummaryService(
        llm,
        FakePromptRepository(),
        context_store,
    )

    return service, llm, context_store


def create_message(
    username="Jane",
    role=MessageRole.USER,
    content="Hello",
):
    return Message(
        username=username,
        role=role,
        content=content,
        conversation_id=uuid4(),
    )


def test_user_summary_workflow():
    service, llm, context_store = create_service()

    user_context = context_store.context_cache["jane"]

    user_context.messages.extend(
        [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hello Jane!"},
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "I'm doing well!"},
        ]
    )

    for _ in range(10):
        service.run(create_message())

    assert llm.summarise_user_current_conversation.call_count == 1
    assert (
        user_context.current_conversation_summary
        == "User conversation summary."
    )
    assert user_context.messages == []

    assert (
        llm.summarise_all_users_current_conversation.call_count
        == 0
    )


def test_global_summary_workflow():
    service, llm, context_store = create_service()

    for _ in range(20):
        service.run(create_message())

    assert llm.summarise_user_current_conversation.call_count == 2
    assert (
        llm.summarise_all_users_current_conversation.call_count
        == 1
    )
    assert (
        context_store.current_meeting_summary
        == "Overall conversation summary."
    )
    assert context_store.current_meeting_conversation == ""