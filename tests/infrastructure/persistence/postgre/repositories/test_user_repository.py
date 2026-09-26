from infrastructure.persistence.postgre.models import User as DBUser
from infrastructure.persistence.postgre.repositories.user_repository import (
    UserRepository,
)


def test_create_user(session):
    repository = UserRepository()

    user = repository.create(session, "Jane")

    assert isinstance(user, DBUser)
    assert user.username == "jane"
    assert user.user_id is not None


def test_get_existing_user(session):
    repository = UserRepository()

    repository.create(session, "Jane")

    user = repository.get(session, "Jane")

    assert user is not None
    assert user.username == "jane"


def test_get_nonexistent_user(session):
    repository = UserRepository()

    user = repository.get(session, "Jane")

    assert user is None