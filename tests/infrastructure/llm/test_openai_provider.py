from unittest.mock import Mock, patch

import pytest

from infrastructure.llm.openai_provider import OpenAIProvider


def create_provider(content: str | None = "Hello from AI_Agent"):
    fake_client = Mock()

    fake_client.chat.completions.create.return_value = Mock(
        choices=[
            Mock(
                message=Mock(content=content)
            )
        ]
    )

    with patch(
        "infrastructure.llm.openai_provider.OpenAI",
        return_value=fake_client,
    ):
        provider = OpenAIProvider(
            api_key="test-key",
            model="test-model",
            reasoning_effort="low",
        )

    return provider, fake_client


def test_missing_api_key():
    with pytest.raises(ValueError, match="API key is missing"):
        OpenAIProvider(
            api_key=None,
            model="test-model",
            reasoning_effort="low",
        )


def test_missing_model():
    with pytest.raises(ValueError, match="model is missing"):
        OpenAIProvider(
            api_key="test-key",
            model=None,
            reasoning_effort="low",
        )


def test_missing_reasoning_effort():
    with pytest.raises(ValueError, match="reasoning effort is missing"):
        OpenAIProvider(
            api_key="test-key",
            model="test-model",
            reasoning_effort=None,
        )


def test_generate_returns_response():
    provider, _ = create_provider()

    prompt = [
        {
            "role": "user",
            "content": "Hello",
        }
    ]

    result = provider.generate(prompt)

    assert result == "Hello from AI_Agent"


def test_generate_raises_when_response_is_empty():
    provider, _ = create_provider(content=None)

    prompt = [
        {
            "role": "user",
            "content": "Hello",
        }
    ]

    with pytest.raises(ValueError, match="empty response"):
        provider.generate(prompt)


def test_summarise_user_current_conversation_formats_messages_correctly():
    provider, fake_client = create_provider()

    prompt_messages = {
        "current_summary": "Previous summary",
        "username": "Jane",
        "messages": [
            {
                "role": "user",
                "content": "Hello",
            },
            {
                "role": "assistant",
                "content": "Hello Jane!",
            },
        ],
        "system": "System prompt",
        "developer": "Developer prompt",
    }

    result = provider.summarise_user_current_conversation(prompt_messages)

    assert result == "Hello from AI_Agent"

    sent_prompt = fake_client.chat.completions.create.call_args.kwargs["messages"]

    assert sent_prompt[0] == {
        "role": "system",
        "content": "System prompt",
    }

    assert sent_prompt[1] == {
        "role": "developer",
        "content": "Developer prompt",
    }

    assert sent_prompt[2] == {
        "role": "user",
        "content": (
            "Previous summary\n"
            "Jane: Hello\n"
            "AI: Hello Jane!\n"
        ),
    }


def test_summarise_all_users_current_conversation_formats_messages_correctly():
    provider, fake_client = create_provider()

    prompt_messages = {
        "current_summary": "Previous overall summary",
        "messages": (
            "jane: Hello\n"
            "AI: Hello Jane!\n"
            "bob: How are you?\n"
            "AI: I'm doing well!\n"
        ),
        "system": "System prompt",
        "developer": "Developer prompt",
    }

    result = provider.summarise_all_users_current_conversation(
        prompt_messages
    )

    assert result == "Hello from AI_Agent"

    sent_prompt = fake_client.chat.completions.create.call_args.kwargs["messages"]

    assert sent_prompt[0] == {
        "role": "system",
        "content": "System prompt",
    }

    assert sent_prompt[1] == {
        "role": "developer",
        "content": "Developer prompt",
    }

    assert sent_prompt[2] == {
        "role": "user",
        "content": (
            "Summary until now:\n"
            "Previous overall summary\n"
            "New messages:\n"
            "jane: Hello\n"
            "AI: Hello Jane!\n"
            "bob: How are you?\n"
            "AI: I'm doing well!\n"
        ),
    }