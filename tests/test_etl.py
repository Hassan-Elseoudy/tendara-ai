import pytest
from sqlalchemy import create_engine, text, StaticPool
from sqlmodel import SQLModel, Session

from tendara_ai_challenge.etl.extractor import JSONDataExtractStrategy, DataExtractService
from tendara_ai_challenge.etl.processor import DataProcessorService, OpenAIAnalyzer
from tendara_ai_challenge.etl.transformer import JSONDataTransformStrategy, DataTransformService
from tendara_ai_challenge.matching.entity import NoticeCategory, NoticeLocation


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_extractor_in_etl():
    """ Test that the JSONDataExtractStrategy class can load data from a JSON file. """
    data_path = "data/notices.json"
    service = DataExtractService(JSONDataExtractStrategy())
    data = service.load(data_path)
    assert len(data) == 2
    assert data[0]["title"] == "Supply and Installation of Solar Panels for Municipal Buildings"
    assert data[1]["title"] == "Construction of New Public Library Facility"

    assert "title" in data[0]
    assert "description" in data[0]
    assert "location" in data[0]
    assert "buyer" in data[0]
    assert "volume" in data[0]
    assert "cpv_codes" in data[0]
    assert "submission_deadline" in data[0]
    assert "submission_deadline" in data[0]


def test_transformer_in_etl():
    """ Test that the JSONDataTransformStrategy class can transform data into a list of Notice objects. """
    data_path = "data/notices.json"
    extract_service = DataExtractService(JSONDataExtractStrategy())
    data = extract_service.load(data_path)

    transform_service = DataTransformService(JSONDataTransformStrategy())
    notices = transform_service.transform_data(data)

    assert len(notices) == 2
    assert notices[0].title == "Supply and Installation of Solar Panels for Municipal Buildings"
    assert notices[1].title == "Construction of New Public Library Facility"

    assert notices[0].description == data[0]["description"]
    assert notices[1].description == data[1]["description"]

    assert notices[0].location == data[0]["location"]
    assert notices[1].location == data[1]["location"]

    assert notices[0].buyer == data[0]["buyer"]
    assert notices[1].buyer == data[1]["buyer"]

    assert notices[0].volume == data[0]["volume"]
    assert notices[1].volume == data[1]["volume"]

    assert notices[0].cpv_codes == data[0]["cpv_codes"]
    assert notices[1].cpv_codes == data[1]["cpv_codes"]


def test_processor_in_etl(session: Session):
    # Add data to the database Category table
    session.exec(text("INSERT INTO category (id, name) VALUES (1, 'Construction')"))
    session.exec(text("INSERT INTO category (id, name) VALUES (2, 'Solar Panels')"))

    # Add data to the database Location table
    session.exec(text("INSERT INTO location (id, city, country) VALUES (1, 'Munich', 'Germany')"))
    session.exec(text("INSERT INTO location (id, city, country) VALUES (2, 'Dublin', 'Ireland')"))

    # Load data from a JSON file
    data_path = "data/notices.json"
    extract_service = DataExtractService(JSONDataExtractStrategy())
    data = extract_service.load(data_path)

    transform_service = DataTransformService(JSONDataTransformStrategy())
    notices = transform_service.transform_data(data)

    # Initialize the data processor with the in-memory database session
    data_processor = DataProcessorService(OpenAIAnalyzer(session))
    data_processor.process(notices)

    # Query the NoticeCategory table to check if the data was processed correctly
    notice_categories = session.query(NoticeCategory).all()

    assert notice_categories[0].notice_id == 1
    assert notice_categories[0].category_id == 2

    assert notice_categories[1].notice_id == 2
    assert notice_categories[1].category_id == 1

    # Query the NoticeLocation table to check if the data was processed correctly
    notice_locations = session.query(NoticeLocation).all()

    assert notice_locations[0].notice_id == 1
    assert notice_locations[0].location_id == 1
