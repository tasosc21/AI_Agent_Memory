from domain.context import Context
from infrastructure.llm.openai_provider import OpenAIProvider


class ConversationService:

    def __init__(self, llm: OpenAIProvider, context: Context) -> None:
        self.llm = llm
        self.context = context

    def run(self) -> str:
        return self.llm.generate(self.context.current_context)