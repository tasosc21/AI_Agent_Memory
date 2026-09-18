from domain.context import Context
from domain.conversation import Conversation
from domain.message import Message
from infrastructure.persistence.postgre.repositories.conversation_repository import ConversationRepository
from infrastructure.persistence.postgre.repositories.message_repository import MessageRepository
from infrastructure.persistence.postgre.repositories.user_repository import UserRepository


class PersistenceService:

    def __init__(
        self,
        context: Context,
        user_repository: UserRepository,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
    ) -> None:
        self.context = context
        self.user_repository = user_repository
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository

    def run(self, message: Message) -> None:
        username = message.username

        if username in self.context.per_user:
            user_context = self.context.per_user[username]
            conversation_id = user_context["conversation"].conversation_id
            message.conversation_id = conversation_id

            self.message_repository.create(message)
            user_context["conversation"].add(message)

        else:
            user = self.user_repository.get(username)

            if not user:
                user = self.user_repository.create(username)

            conversation_record = self.conversation_repository.create(user.user_id)
            context_conversation = Conversation(
                user.username,
                conversation_record.conversation_id,
            )

            message.conversation_id = conversation_record.conversation_id
            context_conversation.add(message)
            self.message_repository.create(message)

            self.context.per_user[username] = {
                "conversation": context_conversation
            }

        # The LLM receives the current user's conversation as its working context.
        self.context.current_context = (
            self.context.per_user[username]["conversation"].conversation
        )