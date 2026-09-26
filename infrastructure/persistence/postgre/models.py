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
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    profile: Mapped[str] = mapped_column(
        Text,
        server_default="",
    )
    summary: Mapped[str] = mapped_column(
        Text,
        server_default="",
    )
    last_interaction_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="user",
    )


class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    meeting_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("meetings.meeting_id"),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.user_id"),
        nullable=False,
    )
    summary: Mapped[str] = mapped_column(
        Text,
        server_default="",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="conversations",
    )
    meeting: Mapped["Meeting"] = relationship(
        back_populates="conversations",
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
    )


class Meeting(Base):
    __tablename__ = "meetings"

    meeting_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    summary: Mapped[str] = mapped_column(
        Text,
        server_default="",
    )
    start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    finish: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="meeting",
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
    role: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages",
    )