from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# Database configuration
# -------------------------

db = os.getenv("DB")
db_name = os.getenv("DB_NAME")
db_role = os.getenv("DB_ROLE")
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"{db}{db_role}:{db_password}@localhost:5432/{db_name}"
)

SessionFactory = sessionmaker(bind=engine)  # Change this