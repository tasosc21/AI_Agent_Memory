from dotenv import load_dotenv

# Load the test environment before importing database.py.
load_dotenv(".env.test", override=True)

import pytest
from sqlalchemy import text

from infrastructure.persistence.postgre.database import SessionFactory, engine


@pytest.fixture
def session(clean_database):
    with SessionFactory() as session:
        yield session


@pytest.fixture
def clean_database():
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE messages, conversations, users, meetings
                RESTART IDENTITY CASCADE
                """
            )
        )