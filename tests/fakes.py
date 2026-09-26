# tests/fakes.py

from types import SimpleNamespace
from uuid import uuid4

from domain.context import Context

from application.context_store import ContextStore
from infrastructure.persistence.txt.prompt_repository import PromptRepository
from infrastructure.llm.openai_provider import OpenAIProvider

from infrastructure.persistence.postgre.repositories.meeting_repository import MeetingRepository
from infrastructure.persistence.postgre.repositories.message_repository import MessageRepository
from infrastructure.persistence.postgre.repositories.conversation_repository import ConversationRepository
from infrastructure.persistence.postgre.repositories.user_repository import UserRepository



class FakeContextStore(ContextStore):

    def __init__(self):
        self.context_cache = {}
        self.current_meeting_conversation = ""
        self.current_meeting_summary = "Current meeting summary"

    def get_user(self, domain_user):
        return self.context_cache.get(domain_user.username)

    def add_user(self, domain_user, domain_conversation):
        context = Context(
            user_id=domain_user.id,
            conversation_id=domain_conversation.id,
            profile=domain_user.profile,
            summary=domain_user.summary,
        )

        self.context_cache[domain_user.username] = context

        return context

    def add_message(self, user_context, domain_message):
        user_context.messages.append(
            {
                "role": domain_message.role.value,
                "content": domain_message.content,
            }
        )

        if domain_message.role.value == "assistant":
            self.current_meeting_conversation += (
                f"AI: {domain_message.content}\n"
            )
        else:
            self.current_meeting_conversation += (
                f"{domain_message.username}: {domain_message.content}\n"
            )


class FakePromptRepository(PromptRepository):
    def get(self, prompt_name):
        prompts = {
            "system": "System prompt",
            "developer": "Developer prompt",
            "summarise_user": "Summarise the user's conversation.",
            "summarise_all_users": "Summarise everyone's conversation.",
            "update_user_profile": "update_user_profile",
            "update_user_summary": "update_user_summary"
        }

        return prompts[prompt_name]


class FakeUserRepository(UserRepository):

    def __init__(self):
        self.users = {}
        self.created_users = []

    def get(self, session, username):
        return self.users.get(username)

    def create(self, session, username):
        user = SimpleNamespace(
            user_id=uuid4(),
            username=username,
            profile="",
            summary="",
        )

        self.users[username] = user
        self.created_users.append(user)

        return user


class FakeConversationRepository(ConversationRepository):

    def __init__(self):
        self.created_conversations = []

    def create(self, session, user_id, meeting_id):
        conversation = SimpleNamespace(
            conversation_id=uuid4(),
            meeting_id=meeting_id,
            user_id=user_id,
            summary="",
        )

        self.created_conversations.append(conversation)

        return conversation


class FakeMessageRepository(MessageRepository):

    def __init__(self):
        self.created_messages = []

    def create(self, session, message):
        db_message = SimpleNamespace(
            role=message.role.value,
            content=message.content,
        )

        self.created_messages.append(message)

        return db_message


class FakeMeetingRepository(MeetingRepository):

    def __init__(self):
        self.created_meetings = []

    def create(self, session):
        meeting = SimpleNamespace(
            meeting_id=uuid4(),
            summary="",
        )

        self.created_meetings.append(meeting)

        return meeting

    def update(self, session, meeting_id):
        pass


class FakeSession:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def begin(self):
        return self


class FakeSessionFactory:

    def __call__(self):
        return FakeSession()

class FakeLLM(OpenAIProvider):

    def __init__(self):
        self.received_context = None

    def get_response(self, full_context):
        self.received_context = full_context
        return "Hello from AI_Agent"