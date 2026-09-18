from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="user"
    )


class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.user_id"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation"
    )


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    conversation_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("conversations.conversation_id"),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(String(10), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages"
    )





# from sqlalchemy import (Column, Uuid, String, Text,
#                         DateTime, ForeignKey, func)
# from sqlalchemy.orm import declarative_base, relationship
# from infrastructure.persistence.postgre.database import engine


# Base = declarative_base()


# # -------------------------
# # User
# # -------------------------

# class User(Base):
#     __tablename__ = "users"
#     user_id = Column(Uuid, primary_key=True, server_default=func.gen_random_uuid())
#     username = Column(String(50), nullable=False)
#     created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
#     conversations = relationship("Conversation", back_populates="user")


# # -------------------------
# # Conversation
# # -------------------------

# class Conversation(Base):
#     __tablename__ = "conversations"
#     conversation_id = Column(Uuid, primary_key=True, server_default=func.gen_random_uuid())
#     user_id = Column(Uuid, ForeignKey("users.user_id"), nullable=False)
#     created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
#     user = relationship("User", back_populates="conversations")
#     messages = relationship("Message", back_populates="conversation")


# # -------------------------
# # Message
# # -------------------------

# class Message(Base):
#     __tablename__ = "messages"
#     message_id = Column(Uuid, primary_key=True, server_default=func.gen_random_uuid())
#     conversation_id = Column(Uuid, ForeignKey("conversations.conversation_id"), nullable=False)
#     role = Column(String(10), nullable=False)
#     content = Column(Text, nullable=False)
#     created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
#     conversation = relationship("Conversation", back_populates="messages")
