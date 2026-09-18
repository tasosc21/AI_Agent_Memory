from dataclasses import dataclass
from uuid import UUID


@dataclass
class Message:

    username: str
    role: str
    content: str
    conversation_id: UUID | None

    def __post_init__(self):
        if self.username:
            self.username = self.username.lower()