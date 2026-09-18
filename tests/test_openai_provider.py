import pytest
from infrastructure.llm.openai_provider import OpenAIProvider

def test_openai_provider_requires_api_key():
    with pytest.raises(ValueError, match="OpenAI API key is missing."):
        OpenAIProvider(
            api_key=None,
            model="some-model",
            reasoning_effort="low",
        )

def test_openai_provider_requires_model():
    with pytest.raises(ValueError, match="OpenAI model is missing."):
        OpenAIProvider(
            api_key="fake-key",
            model=None,
            reasoning_effort="low",
        )

def test_openai_provider_requires_reasoning_effort():
    with pytest.raises(ValueError, match="OpenAI reasoning effort is missing."):
        OpenAIProvider(
            api_key="fake-key",
            model="some-model",
            reasoning_effort=None,
        )