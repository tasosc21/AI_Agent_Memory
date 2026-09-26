from uuid import uuid4

from application.context_store import ContextStore
from domain.context import Context
from domain.conversation import Conversation
from domain.message import Message, MessageRole
from domain.user import User


def test_get_user_returns_cached_context():
    store = ContextStore()

    user = User(uuid4(), "Jane", "", "")
    conversation = Conversation("Jane", uuid4())

    context = store.add_user(user, conversation)

    result = store.get_user(user)

    assert result is context


def test_get_user_returns_none_for_unknown_user():
    store = ContextStore()

    user = User(uuid4(), "Jane", "", "")

    result = store.get_user(user)

    assert result is None


def test_add_user_creates_context():
    store = ContextStore()

    user_id = uuid4()
    conversation_id = uuid4()

    user = User(user_id, "Jane", "", "")
    conversation = Conversation("Jane", conversation_id)

    context = store.add_user(user, conversation)

    assert isinstance(context, Context)
    assert context.user_id == user_id
    assert context.conversation_id == conversation_id
    assert store.context_cache["jane"] is context


def test_add_message_updates_context_and_meeting_conversation():
    store = ContextStore()

    user = User(uuid4(), "Jane", "", "")
    conversation = Conversation("Jane", uuid4())

    context = store.add_user(user, conversation)

    message = Message(
        username="Jane",
        role=MessageRole.USER,
        content="Hello",
        conversation_id=conversation.id,
    )

    store.add_message(context, message)

    assert context.messages == [
        {
            "role": "user",
            "content": "jane: Hello",
        }
    ]

    assert store.current_meeting_conversation == "jane: Hello\n"