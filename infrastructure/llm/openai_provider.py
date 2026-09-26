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

    def generate(self, prompt: list) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=prompt,
            reasoning_effort=self.reasoning_effort,
        )

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("OpenAI returned an empty response.")

        return content


    def summarise_user_current_conversation(self, prompt_messages: dict) -> str:
        message_prompt = f"{prompt_messages["current_summary"]}\n"

        for message in prompt_messages["messages"]:
            if message["role"] == "user":
                message_prompt += f"{prompt_messages["username"]}: {message["content"]}\n"
            else:
                message_prompt += f"AI: {message["content"]}\n"

        full_prompt = [
            {"role": "system", "content": prompt_messages["system"]},
            {"role": "developer", "content": prompt_messages["developer"]},
            {"role": "user", "content": message_prompt}
            ]

        return self.generate(full_prompt)

    def summarise_all_users_current_conversation(self, prompt_messages: dict) -> str:
        message_prompt = (
            f"Summary until now:\n{prompt_messages["current_summary"]}\n"
            f"New messages:\n{prompt_messages["messages"]}")

        full_prompt = [
            {"role": "system", "content": prompt_messages["system"]},
            {"role": "developer", "content": prompt_messages["developer"]},
            {"role": "user", "content": message_prompt}
            ]

        return self.generate(full_prompt)

    def get_response(self, prompt_messages: dict) -> str:
        full_prompt = [
            {"role": "system", "content": prompt_messages["system"]},
            {"role": "developer", "content": prompt_messages["developer"]},
            {"role": "user",
             "content": (f"This is user's {prompt_messages["username"]} personal profile.\n"
                         f"{prompt_messages["profile"]}\n"
                         f"This is user's {prompt_messages["username"]} personal summary.\n"
                         f"{prompt_messages["user_summary"]}\n")},
            {"role": "user",
             "content": ("This is the current summary of the conversation with this user:\n"
                         f"{prompt_messages["conversation_summary"]}\n\n"
                         "This is the current summary of the overall conversation with all users:\n"
                         f"{prompt_messages["meeting_summary"]}\n{prompt_messages["meeting_messages"]}")}
                         ]
        full_prompt += prompt_messages["messages"]

        return self.generate(full_prompt)

    def update_profile(self, prompt_messages: dict) -> str:
        full_prompt = [
            {"role": "system", "content":prompt_messages["system"]},
            {"role": "developer", "content": prompt_messages["developer"]},
            {"role": "user",
             "content": ("Existing profile:\n"
                         f"{prompt_messages["profile"]}"
                         "Current conversation summary:"
                         f"{prompt_messages["conversation_summary"]}"
                         "Return only the updated profile as plain text.")}]
        return self.generate(full_prompt)
    
    def update_summary(self, prompt_messages: dict) -> str:
        full_prompt = [
            {"role": "system", "content":prompt_messages["system"]},
            {"role": "developer", "content": prompt_messages["developer"]},
            {"role": "user",
             "content": ("Existing summary:\n"
                         f"{prompt_messages["summary"]}"
                         "Current conversation summary:"
                         f"{prompt_messages["conversation_summary"]}"
                         "Return only the updated profile as plain text.")
                         }]
        return self.generate(full_prompt)