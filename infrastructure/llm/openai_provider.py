from typing import cast

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from openai.types.shared import ReasoningEffort


class OpenAIProvider:

    def __init__(
        self,
        api_key: str | None,
        model: str | None,
        reasoning_effort: ReasoningEffort | None,
    ) -> None:
        
        if not api_key:
            raise ValueError("OpenAI API key is missing.")

        if not model:
            raise ValueError("OpenAI model is missing.")

        if not reasoning_effort:
            raise ValueError("OpenAI reasoning effort is missing.")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.reasoning_effort: ReasoningEffort = reasoning_effort

    def generate(self, messages: list[dict[str, str]]) -> str:
        openai_messages = [
            cast(ChatCompletionMessageParam, message)
            for message in messages
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            reasoning_effort=self.reasoning_effort,
        )

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("OpenAI returned an empty response.")

        return content