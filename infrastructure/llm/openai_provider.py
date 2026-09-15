from typing import cast

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

class OpenAIProvider:

    def __init__(self, api_key: str | None, model: str | None):
        if not api_key:
            raise ValueError("OpenAI API key is missing.")

        if not model:
            raise ValueError("OpenAI model is missing.")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, messages: list[dict[str, str]]):
        openai_messages = [
            cast(ChatCompletionMessageParam, message)
            for message in messages
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            reasoning_effort='low'
        )

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("OpenAI returned an empty response.")

        return content


"""
OpenAI Response

ChatCompletion(id='chatcmpl-ENJIC0Ba8F5xLTZhJM4R4rQcQNkoy', 
choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Hey Dayo! Great to hear from you. How can I help today? If you want translations, Yoruba language tips, or help with any topic, just tell me what you need.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], 
created=1789224412, 
model='gpt-5-nano-2025-08-07', 
object='chat.completion', 
metadata=None, 
moderation=None, 
service_tier='default', 
system_fingerprint=None, 
usage=CompletionUsage(completion_tokens=944, prompt_tokens=11, total_tokens=955, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=896, rejected_prediction_tokens=0, text_tokens=None), 
prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cache_write_tokens=None, cached_tokens=0, image_tokens=None, text_tokens=None)))
"""