from infrastructure.persistence.postgre.repositories.conversation_repository import (
    ConversationRepository,
)
from infrastructure.persistence.postgre.repositories.user_repository import (
    UserRepository,
)

from uuid import UUID
import pytest
from sqlalchemy.exc import IntegrityError


def test_create_conversation():
    user_repository = UserRepository()
    conversation_repository = ConversationRepository()

    user = user_repository.create("TestUser")

    conversation = conversation_repository.create(user.user_id)

    assert conversation.conversation_id is not None
    assert conversation.user_id == user.user_id
    assert conversation.created_at is not None


def test_conversation_belongs_to_correct_user():
    user_repository = UserRepository()
    conversation_repository = ConversationRepository()

    user = user_repository.create("TestUser")

    conversation = conversation_repository.create(user.user_id)

    assert conversation.user_id == user.user_id


def test_get():
    user_repository = UserRepository()
    conversation_repository = ConversationRepository()

    user = user_repository.create("TestUser")
    conversation = conversation_repository.create(user.user_id)

    messages = conversation_repository.get(
        conversation.conversation_id
    )

    assert messages == []


def test_messages_are_returned_in_chronological_order_n_correct_format():
    user_repository = UserRepository()
    conversation_repository = ConversationRepository()

    user = user_repository.create("TestUser")
    conversation = conversation_repository.create(user.user_id)

    # We'll insert messages directly for this test because
    # we're testing ConversationRepository.get_messages().
    from infrastructure.persistence.postgre.models import Message

    from infrastructure.persistence.postgre.database import SessionFactory

    with SessionFactory() as session:
        first = Message(
            conversation_id=conversation.conversation_id,
            role="user",
            content="First",
        )
        second = Message(
            conversation_id=conversation.conversation_id,
            role="assistant",
            content="Second",
        )

        session.add_all([first, second])
        session.commit()

    messages = conversation_repository.get(
        conversation.conversation_id
    )

    assert messages == [{"role": "user", "content": "First"},
                        {"role": "assistant", "content": "Second"}]


def test_cannot_create_conversation_for_nonexistent_user():
    repository = ConversationRepository()

    nonexistent_user_id = UUID(
        "00000000-0000-0000-0000-000000000000"
    )

    with pytest.raises(IntegrityError):
        repository.create(nonexistent_user_id)