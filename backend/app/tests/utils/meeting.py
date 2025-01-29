from sqlmodel import Session

from app import crud
from app.models import Meeting, MeetingCreate
from app.tests.utils.utils import random_lower_string


def create_random_meeting(db: Session) -> Meeting:
    title = random_lower_string()
    agenda = random_lower_string()
    summary = random_lower_string()
    meeting_in = MeetingCreate(title=title, agenda=agenda, summary=summary)
    return crud.create_meeting(session=db, meeting_in=meeting_in)
