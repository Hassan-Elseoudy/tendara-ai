import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from tendara_ai_challenge.matching.entity import Profile, get_session
from tendara_ai_challenge.profile.app import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_profile_should_return_profile(client: TestClient):
    profile = {
        "location_id": 1,
        "category_id": 1,
        "tag_ids": [1, 2, 3],
    }
    response = client.post("/profiles", json=profile)
    assert response.status_code == 200
    assert response.json()["location_id"] == profile["location_id"]
    assert response.json()["category_id"] == profile["category_id"]
    assert response.json()["tags"] == profile["tag_ids"]


def test_read_profile_should_return_profile(client: TestClient, session: Session):
    profile = {
        "location_id": 1,
        "category_id": 1,
        "tag_ids": [1, 2, 3],
    }
    response = client.post("/profiles", json=profile)
    profile_id = response.json()["id"]

    response = client.get(f"/profiles/{profile_id}")
    assert response.status_code == 200
    assert response.json()["location_id"] == profile["location_id"]
    assert response.json()["category_id"] == profile["category_id"]
    assert response.json()["tags"] == profile["tag_ids"]


def test_read_profile_should_return_404_when_profile_not_found(client: TestClient):
    response = client.get("/profiles/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"


def test_delete_profile_should_return_200(client: TestClient, session: Session):
    profile = {
        "location_id": 1,
        "category_id": 1,
        "tag_ids": [1, 2, 3],
    }
    response = client.post("/profiles", json=profile)
    profile_id = response.json()["id"]

    response = client.delete(f"/profiles/{profile_id}")
    assert response.status_code == 200

    profile = session.query(Profile).filter_by(id=profile_id).first()
    assert profile is None


def test_delete_profile_should_return_404_when_profile_not_found(client: TestClient):
    response = client.delete("/profiles/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"
