from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:

    id: UUID
    username: str
    profile: str
    summary: str

    def __post_init__(self):
        if self.username:
            self.username = self.username.lower()