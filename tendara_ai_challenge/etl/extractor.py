import json
from abc import ABC, abstractmethod
from typing import List


class DataExtractStrategy(ABC):
    @abstractmethod
    def load_data(self, data_source: str) -> List[dict]:
        pass


class JSONDataExtractStrategy(DataExtractStrategy):
    def load_data(self, data_path: str) -> List[dict]:
        with open(data_path, 'r') as f:
            data = json.load(f)
        return data


class APIDataExtractStrategy(DataExtractStrategy):
    def load_data(self, api_url: str) -> List[dict]:
        # TODO("Implement API data extraction logic if needed")
        pass


class DataExtractService:
    def __init__(self, strategy: DataExtractStrategy):
        self.strategy = strategy

    def load(self, data_source) -> List[dict]:
        notices = self.strategy.load_data(data_source)
        # TODO: Add data validation logic here and ignore invalid data
        return notices
