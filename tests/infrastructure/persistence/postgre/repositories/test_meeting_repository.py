from infrastructure.persistence.postgre.models import Meeting as DBMeeting
from infrastructure.persistence.postgre.repositories.meeting_repository import (
    MeetingRepository,
)


def test_create_meeting(session):
    repository = MeetingRepository()

    meeting = repository.create(session)

    assert isinstance(meeting, DBMeeting)
    assert meeting.meeting_id is not None
    assert meeting.finish is None


def test_update_meeting(session):
    repository = MeetingRepository()

    meeting = repository.create(session)

    repository.update(session, meeting.meeting_id, meeting.summary)

    session.flush()
    session.refresh(meeting)

    assert meeting.finish is not None