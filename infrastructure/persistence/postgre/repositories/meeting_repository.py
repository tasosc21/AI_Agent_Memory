from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select, update, func
from sqlalchemy.orm import Session

from infrastructure.persistence.postgre.models import Meeting as DBMeeting


class MeetingRepository:

    def create(self, session: Session) -> DBMeeting:
        dbmeeting = DBMeeting()
        session.add(dbmeeting)
        session.flush()

        return dbmeeting

    def update(self, session: Session, meeting_id: UUID, meeting_summary: str) -> None:
        statement = (
            update(DBMeeting)
            .where(DBMeeting.meeting_id == meeting_id)
            .values(
                finish=func.now(), 
                summary=meeting_summary         
            )
        )
        session.execute(statement)       
