from uuid import UUID

from domain.message import Message


class Conversation:

    def __init__(self, username: str, conversation_id: UUID | None) -> None:
        self.username = username.lower()
        self.id = conversation_id
        self.conversation: list[dict[str, str]] = []

    def add(self, message: Message) -> None:
        formatted_message = {
            "role": message.role.value,
            "content": message.content,
        }

        self.conversation.append(formatted_message)