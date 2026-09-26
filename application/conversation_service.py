from infrastructure.llm.openai_provider import OpenAIProvider


class ConversationService:

    def __init__(self, llm: OpenAIProvider) -> None:
        self.llm = llm

    def run(self, full_context: dict) -> str:
        if not full_context:
            raise ValueError("Context cannot be empty.")

        return self.llm.get_response(full_context)