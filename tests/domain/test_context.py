from uuid import uuid4

from domain.context import Context


def test_context_creation():
    user_id = uuid4()
    conversation_id = uuid4()

    context = Context(
        user_id=user_id,
        conversation_id=conversation_id,
        profile="",
        summary="",
    )

    assert context.user_id == user_id
    assert context.conversation_id == conversation_id
    assert context.messages == []
    assert context.profile == ""
    assert context.summary == ""
    assert context.current_conversation_summary == ""