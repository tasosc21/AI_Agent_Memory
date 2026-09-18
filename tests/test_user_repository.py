from infrastructure.persistence.postgre.repositories.user_repository import (
    UserRepository,
)


def test_create():
    repository = UserRepository()

    user = repository.create("TestUser")

    assert user.user_id is not None
    assert user.username == "testuser"
    assert user.created_at is not None


def test_get_existing_user():
    repository = UserRepository()

    repository.create("TestUser")

    user = repository.get("testuser")

    assert user is not None
    assert user.username == "testuser"


def test_get_missing_user_returns_none():
    repository = UserRepository()

    user = repository.get("does_not_exist")

    assert user is None