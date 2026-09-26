from uuid import uuid4

from domain.user import User


def test_username_is_lowercase():
    user = User(
        id=uuid4(),
        username="JaNe",
        profile="",
        summary="",
    )

    assert user.username == "jane"