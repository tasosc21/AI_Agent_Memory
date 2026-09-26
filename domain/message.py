from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class Message:
    username: str
    role: MessageRole
    content: str
    conversation_id: UUID | None

    def __post_init__(self) -> None:
        self.username = self.username.lower()