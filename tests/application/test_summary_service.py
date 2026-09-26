from unittest.mock import Mock
from uuid import uuid4

from application.summary_service import SummaryService
from domain.context import Context
from domain.message import Message, MessageRole
from tests.fakes import FakeContextStore, FakePromptRepository


def create_service():
    llm = Mock()

    llm.summarise_user_current_conversation.return_value = (
        "Updated user conversation summary."
    )

    llm.summarise_all_users_current_conversation.return_value = (
        "Updated global conversation summary."
    )

    context_store = FakeContextStore()

    context = Context(
        user_id=uuid4(),
        conversation_id=uuid4(),
        profile="",
        summary="",
    )

    context.current_conversation_summary = "Previous user summary"

    context_store.context_cache["jane"] = context
    context_store.current_meeting_summary = "Previous global summary"

    service = SummaryService(
        llm,
        FakePromptRepository(),
        context_store,
    )

    return service, llm, context_store


def create_message(username="Jane"):
    return Message(
        username=username,
        role=MessageRole.USER,
        content="Hello",
        conversation_id=uuid4(),
    )


def test_run_counts_user_interactions():
    service, _, _ = create_service()

    service.run(create_message())
    service.run(create_message())

    assert service.user_interactions["jane"] == 2
    assert service.total_user_interactions == 2


def test_user_summary_is_generated_every_10_interactions():
    service, llm, context_store = create_service()

    for _ in range(10):
        service.run(create_message())

    user_context = context_store.context_cache["jane"]

    assert llm.summarise_user_current_conversation.call_count == 1
    assert (
        user_context.current_conversation_summary
        == "Updated user conversation summary."
    )


def test_user_messages_are_cleared_after_user_summary():
    service, _, context_store = create_service()

    for _ in range(10):
        service.run(create_message())

    user_context = context_store.context_cache["jane"]

    assert user_context.messages == []


def test_user_summary_is_not_generated_before_10_interactions():
    service, llm, context_store = create_service()

    user_context = context_store.context_cache["jane"]

    user_context.messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hello Jane!"},
    ]

    for _ in range(9):
        service.run(create_message())

    assert llm.summarise_user_current_conversation.call_count == 0
    assert (
        user_context.current_conversation_summary
        == "Previous user summary"
    )
    assert len(user_context.messages) == 2


def test_global_summary_is_generated_every_20_interactions():
    service, llm, context_store = create_service()

    for _ in range(20):
        service.run(create_message())

    assert llm.summarise_all_users_current_conversation.call_count == 1
    assert (
        context_store.current_meeting_summary
        == "Updated global conversation summary."
    )


def test_meeting_conversation_is_cleared_after_global_summary():
    service, _, context_store = create_service()

    for _ in range(20):
        service.run(create_message())

    assert context_store.current_meeting_conversation == ""


def test_global_summary_is_not_generated_before_20_interactions():
    service, llm, context_store = create_service()

    for _ in range(19):
        service.run(create_message())

    assert llm.summarise_all_users_current_conversation.call_count == 0


def test_user_interactions_are_tracked_separately():
    service, _, _ = create_service()

    service.run(create_message("Jane"))
    service.run(create_message("Bob"))
    service.run(create_message("Jane"))

    assert service.user_interactions["jane"] == 2
    assert service.user_interactions["bob"] == 1
    assert service.total_user_interactions == 3


def test_on_exit_summarises_users_with_unsummarised_messages():
    service, llm, context_store = create_service()

    user_context = context_store.context_cache["jane"]

    user_context.messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hello Jane!"},
    ]

    service.on_exit()

    llm.summarise_user_current_conversation.assert_called_once()

    assert (
        user_context.current_conversation_summary
        == "Updated user conversation summary."
    )


def test_on_exit_does_not_summarise_user_without_messages():
    service, llm, context_store = create_service()

    user_context = context_store.context_cache["jane"]
    user_context.messages = []

    service.on_exit()

    llm.summarise_user_current_conversation.assert_not_called()


def test_on_exit_summarises_meeting_with_unsummarised_messages():
    service, llm, context_store = create_service()

    context_store.current_meeting_conversation = (
        "jane: Hello\n"
        "AI: Hello Jane!\n"
    )

    service.on_exit()

    llm.summarise_all_users_current_conversation.assert_called_once()

    assert (
        context_store.current_meeting_summary
        == "Updated global conversation summary."
    )


def test_on_exit_does_not_summarise_empty_meeting():
    service, llm, context_store = create_service()

    context_store.current_meeting_conversation = ""

    service.on_exit()

    llm.summarise_all_users_current_conversation.assert_not_called()