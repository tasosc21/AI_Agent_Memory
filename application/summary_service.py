from infrastructure.llm.openai_provider import OpenAIProvider
from infrastructure.persistence.txt.prompt_repository import PromptRepository

from application.context_store import ContextStore

from domain.message import Message as DomainMessage

class SummaryService:

    def __init__(self, llm: OpenAIProvider, prompt_repository: PromptRepository, context_store: ContextStore) -> None:
        self.llm = llm
        self.prompt_repository = prompt_repository
        self.context_store = context_store
        self.prompts = self.get_prompts()
        self.user_interactions: dict[str, int] = {}
        self.total_user_interactions = 0

    def run(self, domain_user_message: DomainMessage):

        username = domain_user_message.username
        self.user_interactions[username] = self.user_interactions.get(username, 0) + 1
        self.total_user_interactions += 1

        if self.user_interactions[username] % 10 == 0:
            user_context = self.context_store.context_cache[username]
            user_context.current_conversation_summary = self.llm.summarise_user_current_conversation(
                {"system": self.prompts["summarise_user"],
                 "developer": '',
                 "current_summary": user_context.current_conversation_summary,
                 "messages": user_context.messages,
                 "username": username})
             
            user_context.messages = []

        if self.total_user_interactions % 20 == 0:
            self.context_store.current_meeting_summary = self.llm.summarise_all_users_current_conversation(
                {"system": self.prompts["summarise_all_users"],
                 "developer": "",
                 "current_summary": self.context_store.current_meeting_summary,
                 "messages": self.context_store.current_meeting_conversation
                 })

            self.context_store.current_meeting_conversation = ""


    def get_prompts(self):
        summarise_user = self.prompt_repository.get("summarise_user")
        summarise_all_user = self.prompt_repository.get("summarise_all_users")
        update_user_profile = self.prompt_repository.get("update_user_profile")
        update_user_summary = self.prompt_repository.get("update_user_summary")

        return {"summarise_user": summarise_user,
                "summarise_all_users": summarise_all_user,
                "update_user_profile": update_user_profile,
                "update_user_summary": update_user_summary
                }

    def on_exit(self):
        for key, value in self.context_store.context_cache.items():
            if len(value.messages) != 0:  
                value.current_conversation_summary = self.llm.summarise_user_current_conversation(
                    {"system": self.prompts["summarise_user"],
                    "developer": '',
                    "current_summary": value.current_conversation_summary,
                    "messages": value.messages,
                    "username": key})

            value.profile = self.llm.update_profile(
                {"system": self.prompts["update_user_profile"],
                 "developer": "",
                 "profile": value.profile,
                 "conversation_summary": value.current_conversation_summary,
                 "username": key
                }
            )

            value.summary = self.llm.update_summary(
                {"system": self.prompts["update_user_summary"],
                 "developer": "",
                 "summary": value.summary,
                 "conversation_summary": value.current_conversation_summary,
                 "username": key
                }
            )

        if self.context_store.current_meeting_conversation != "":
                self.context_store.current_meeting_summary = self.llm.summarise_all_users_current_conversation(
                    {"system": self.prompts["summarise_all_users"],
                    "developer": "",
                    "current_summary": self.context_store.current_meeting_summary,
                    "messages": self.context_store.current_meeting_conversation
                    })
