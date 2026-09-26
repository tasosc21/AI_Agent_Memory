from application.conversation_service import ConversationService
from tests.fakes import FakeLLM
import pytest


def test_run_sends_context_to_llm():
    llm = FakeLLM()
    service = ConversationService(llm)

    context = {
        "username": "jane",
        "messages": [],
    }

    result = service.run(context)

    assert result == "Hello from AI_Agent"
    assert llm.received_context == context


def test_run_rejects_empty_context():
    llm = FakeLLM()
    service = ConversationService(llm)

    with pytest.raises(ValueError, match="Context cannot be empty"):
        service.run({})