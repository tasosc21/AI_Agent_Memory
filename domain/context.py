from uuid import UUID


class Context:

    def __init__(self, user_id: UUID, profile: str, summary: str, conversation_id: UUID|None = None) -> None:
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.messages: list[dict[str, str]] = []
        self.profile = profile
        self.summary = summary
        self.current_conversation_summary = ''