from uuid import UUID

from domain.context import Context
from domain.user import User as DomainUser
from domain.message import Message as DomainMessage
from domain.message import MessageRole
from domain.conversation import Conversation as DomainConversation


class ContextStore:

    def __init__(self) -> None:
        self.context_cache: dict[str, Context] = {}
        empty_uuid = UUID(int=0)

        self.current_meeting_conversation = ""
        self.current_meeting_summary = ""

    def get_user(self, domain_user: DomainUser) -> Context | None:
        return self.context_cache.get(domain_user.username)

    def add_user(
        self,
        domain_user: DomainUser,
        domain_conversation: DomainConversation,
    ) -> Context:
        context = Context(
            user_id=domain_user.id,
            conversation_id=domain_conversation.id,
            profile=domain_user.profile,
            summary=domain_user.summary
        )

        self.context_cache[domain_user.username] = context

        return context

    def add_message(
        self,
        user_context: Context,
        domain_message: DomainMessage,
    ) -> None:
        new_message = {
            "role": domain_message.role.value,
            "content": f"{domain_message.username}: {domain_message.content}",
        }

        user_context.messages.append(new_message)

        if domain_message.role == MessageRole.ASSISTANT:
            self.current_meeting_conversation += (
                f"AI: {domain_message.content}\n"
            )
        else:
            self.current_meeting_conversation += (
                f"{domain_message.username}: {domain_message.content}\n"
            )