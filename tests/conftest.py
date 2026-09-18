from dotenv import load_dotenv

import pytest
from sqlalchemy import text

from infrastructure.persistence.postgre.database import engine


load_dotenv(".env.test", override=True)


@pytest.fixture(autouse=True)
def clean_database():
    yield

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE messages, conversations, users
                RESTART IDENTITY CASCADE
                """
            )
        )