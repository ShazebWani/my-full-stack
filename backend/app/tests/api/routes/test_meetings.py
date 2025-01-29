from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.meeting import create_random_meeting


# Shazeb's note: Don't need permissions for meetings because we don't check
# if the user is super user like we do for items

def test_create_meeting(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"title": "Test Meeting", "agenda": "Test Agenda", "summary": "Test Summary"}
    response = client.post(
        f"{settings.API_V1_STR}/meetings/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["agenda"] == data["agenda"]
    assert content["summary"] == data["summary"]
    assert "id" in content


def test_read_meeting(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    meeting = create_random_meeting(db)
    response = client.get(
        f"{settings.API_V1_STR}/meetings/{meeting.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == meeting.title
    assert content["agenda"] == meeting.agenda
    assert content["summary"] == meeting.summary
    assert content["id"] == meeting.id


def test_read_meeting_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/meetings/12345678",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Meeting not found"


def test_read_meetings(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_meeting(db)
    create_random_meeting(db)
    response = client.get(
        f"{settings.API_V1_STR}/meetings/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_meeting(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    meeting = create_random_meeting(db)
    data = {"title": "Updated Meeting", "agenda": "Updated agenda", "summary": "Updated summary"}
    response = client.put(
        f"{settings.API_V1_STR}/meetings/{meeting.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["agenda"] == data["agenda"]
    assert content["summary"] == data["summary"]
    assert content["id"] == meeting.id

def test_update_meeting_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"title": "Nonexistent Meeting", "agenda": "Nonexistent agenda", "summary": "Nonexistent summary"}
    response = client.put(
        f"{settings.API_V1_STR}/meetings/1234567",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Meeting not found"


def test_delete_meeting(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    meeting = create_random_meeting(db)
    response = client.delete(
        f"{settings.API_V1_STR}/meetings/{meeting.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Meeting deleted successfully"


def test_delete_meeting_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/meetings/12345678",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Meeting not found"
