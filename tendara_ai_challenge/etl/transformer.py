from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from tendara_ai_challenge.matching.dto import NoticeModel


class DataTransformStrategy(ABC):
    @abstractmethod
    def transform(self, data: List[dict]) -> List[NoticeModel]:
        pass


class JSONDataTransformStrategy(DataTransformStrategy):
    def transform(self, data: List[dict]) -> List[NoticeModel]:
        notices = []
        for notice_data in data:
            notice = NoticeModel(**notice_data)
            notice.publication_deadline = datetime.fromisoformat(notice_data["publication_deadline"])
            notice.submission_deadline = datetime.fromisoformat(notice_data["submission_deadline"])
            notices.append(notice)
        return notices


class DataTransformService:
    def __init__(self, strategy: DataTransformStrategy):
        self.strategy = strategy

    def transform_data(self, data: List[dict]) -> List[NoticeModel]:
        return self.strategy.transform(data)
