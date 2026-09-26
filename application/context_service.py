from application.context_store import ContextStore
from application.types import PersistenceResult
from infrastructure.persistence.txt.prompt_repository import PromptRepository


class ContextService:

    def __init__(
        self,
        context_store: ContextStore,
        prompt_repository: PromptRepository,
    ) -> None:
        self.context_store = context_store
        self.prompt_repository = prompt_repository

    def run(self, domain_objects: PersistenceResult) -> dict:
        user_context = self.context_store.get_user(domain_objects["user"])

        if not user_context:
            user_context = self.context_store.add_user(
                domain_objects["user"],
                domain_objects["conversation"],
            )

        self.context_store.add_message(
            user_context,
            domain_objects["message"],
        )

        full_context = {
            "username": domain_objects["user"].username,
            "profile": user_context.profile,
            "user_summary": user_context.summary,
            "meeting_summary": self.context_store.current_meeting_summary,
            "meeting_messages": self.context_store.current_meeting_conversation,
            "conversation_summary": user_context.current_conversation_summary,
            "messages": user_context.messages,
            "system": self.prompt_repository.get("system"),
            "developer": self.prompt_repository.get("developer"),
        }

        return full_context