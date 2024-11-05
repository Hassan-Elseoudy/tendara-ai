import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from tendara_ai_challenge.matching.app import app
from tendara_ai_challenge.matching.entity import get_session


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


def test_should_match_if_same_category_location_tags(client: TestClient, session: Session):
    # Create some categories and save it to the database
    session.exec(text("INSERT INTO category (id, name) VALUES (1, 'Construction')"))
    session.exec(text("INSERT INTO category (id, name) VALUES (2, 'Solar Panels')"))
    session.exec(text("INSERT INTO category (id, name) VALUES (3, 'IT')"))

    # Create some locations and save it to the database
    session.exec(text("INSERT INTO location (id, city, country) VALUES (1, 'Alexandria', 'Egypt')"))
    session.exec(text("INSERT INTO location (id, city, country) VALUES (2, 'Oxford', 'UK')"))
    session.exec(text("INSERT INTO location (id, city, country) VALUES (3, 'Berlin', 'Germany')"))

    # Create some notices and save it to the database
    ## Solar Panels notice
    session.exec(text("INSERT INTO notice (id, title, description, publication_deadline) "
                      "VALUES (1, "
                      "'Supply and Installation of Solar Panels for Municipal Buildings', "
                      "'Seeking qualified contractors to supply and install photovoltaic solar panels on multiple municipal buildings to enhance renewable energy usage and reduce carbon footprint. The project includes maintenance services for a period of 5 years.', "
                      "'2022-12-31')"))

    ## IT notice
    session.exec(text("INSERT INTO notice (id, title, description, publication_deadline) "
                      "VALUES (2, "
                      "'Python Developer for Web Development', "
                      "'Looking for a Python developer to work on web development projects. The candidate should have experience in Django, Flask, and other web frameworks.', "
                      "'2022-12-31')"))

    ## Construction notice
    session.exec(text("INSERT INTO notice (id, title, description, publication_deadline) "
                      "VALUES (3, "
                      "'Construction of a New Office Building', "
                      "'Seeking qualified contractors to construct a new office building. The project includes civil, mechanical, and structural works.', "
                      "'2022-12-31')"))

    # Create some notice categories and save it to the database
    session.exec(text("INSERT INTO noticecategory (notice_id, category_id) VALUES (1, 2)"))  # Solar Panels
    session.exec(text("INSERT INTO noticecategory (notice_id, category_id) VALUES (2, 3)"))  # IT
    session.exec(text("INSERT INTO noticecategory (notice_id, category_id) VALUES (3, 1)"))  # Construction

    # Create some notice locations and save it to the database
    session.exec(text("INSERT INTO noticelocation (notice_id, location_id) VALUES (1, 2)"))  # Oxford, UK
    session.exec(text("INSERT INTO noticelocation (notice_id, location_id) VALUES (2, 3)"))  # Berlin, Germany
    session.exec(text("INSERT INTO noticelocation (notice_id, location_id) VALUES (3, 1)"))  # Alexandria, Egypt

    # Create some profiles and save it to the database
    ## IT profile
    session.exec(text("INSERT INTO profile (id, category_id, location_id, tags, publication_deadline) "
                      "VALUES (1, 3, 3, 'Python,Java,C++', '2022-12-31')"))
    ## Construction profile
    session.exec(text("INSERT INTO profile (id, category_id, location_id, tags, publication_deadline) "
                      "VALUES (2, 1, 1, 'Civil,Mechanical,Structural', '2022-12-31')"))
    ## Solar Panels profile
    session.exec(text("INSERT INTO profile (id, category_id, location_id, tags, publication_deadline) "
                      "VALUES (3, 2, 2, 'Solar,Energy,Renewable', '2022-12-31')"))

    response = client.get("profiles/1/matches")
    assert response.status_code == 200
    assert response.json()["notices"][0]["id"] == 2  # IT notice

    response = client.get("profiles/2/matches")
    assert response.status_code == 200
    assert response.json()["notices"][0]["id"] == 3  # Construction notice

    response = client.get("profiles/3/matches")
    assert response.status_code == 200
    assert response.json()["notices"][0]["id"] == 1  # Solar Panels notice
