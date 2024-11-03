from tendara_ai_challenge.etl.extractor import JSONDataExtractStrategy, DataExtractService


def test_extractor_in_etl():
    """ Test that the JSONDataExtractStrategy class can load data from a JSON file. """
    data_path = "data/notices.json"
    strategy = DataExtractService(JSONDataExtractStrategy())
    data = strategy.load(data_path)
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
