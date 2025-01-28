from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Meeting,
    MeetingCreate,
    MeetingPublic,
    MeetingsPublic,
    MeetingUpdate,
    Message,
)

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.get("/", response_model=MeetingsPublic)
def read_meetings(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve meetings.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Meeting)
        count = session.exec(count_statement).one()
        statement = select(Meeting).offset(skip).limit(limit)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    meetings = session.exec(statement).all()
    return MeetingsPublic(data=meetings, count=count)


@router.get("/{id}", response_model=MeetingPublic)
def read_meeting(
    session: SessionDep, current_user: CurrentUser, id: int
) -> Any:
    """
    Get meeting by ID.
    """
    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return meeting


@router.post("/", response_model=MeetingPublic)
def create_meeting(
    *, session: SessionDep, current_user: CurrentUser, meeting_in: MeetingCreate
) -> Any:
    """
    Create new meeting.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    meeting = Meeting(
        title=meeting_in.title,
        agenda=meeting_in.agenda,
        summary=meeting_in.summary,
    )
    session.add(meeting)
    session.commit()
    session.refresh(meeting)
    return meeting


@router.put("/{id}", response_model=MeetingPublic)
def update_meeting(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: int,
    meeting_in: MeetingUpdate,
) -> Any:
    """
    Update a meeting.
    """
    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = meeting_in.model_dump(exclude_unset=True)
    meeting.sqlmodel_update(update_dict)
    session.add(meeting)
    session.commit()
    session.refresh(meeting)
    return meeting


@router.delete("/{id}")
def delete_meeting(
    session: SessionDep, current_user: CurrentUser, id: int
) -> Message:
    """
    Delete a meeting.
    """
    meeting = session.get(Meeting, id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(meeting)
    session.commit()
    return Message(message="Meeting deleted successfully")
