import logging
import os
from abc import ABC, abstractmethod
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI

from tendara_ai_challenge.etl.dto import RelatedIds
from tendara_ai_challenge.matching.alchemy import Category, Notice, NoticeCategory, Location, NoticeLocation
from tendara_ai_challenge.matching.dto import NoticeModel

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


class Analyzer(ABC):

    def __init__(self, database):
        self.database = database

    @abstractmethod
    def fetch_related_ids(self, categories: List[Category], locations: List[Location], notice: NoticeModel) -> Optional[RelatedIds]:
        pass


class OpenAIAnalyzer(Analyzer):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = """
    Given the following notice, predict the category (ies) and location(s) that best match the notice:
    Categories: %s
    Locations: %s
    Notice: %s
    return the ids of the categories and locations that best match the notice.
    """

    def fetch_related_ids(self, categories: List[Category], locations: List[Location], notice: NoticeModel) -> Optional[RelatedIds]:
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": self.prompt % (categories, locations, notice.description + " " + notice.title)}
            ],
            response_format=RelatedIds
        )
        analysis_result_message = response.choices[0].message
        if not analysis_result_message.refusal:
            logging.info("AI provided the analysis, returning the ids %s", analysis_result_message.parsed)
            return analysis_result_message.parsed

        logging.error("AI refused to provide the analysis")
        return None


class DataProcessorService:

    def __init__(self, analyzer: Analyzer):
        self.analyzer = analyzer

    def process(self, notices: List[NoticeModel]) -> List[Notice]:
        categories = self.analyzer.database.query(Category).all()
        locations = self.analyzer.database.query(Location).all()
        notice_entities = []

        for notice in notices:
            related_ids: Optional[RelatedIds] = self.analyzer.fetch_related_ids(categories, locations, notice)
            notice_entity = Notice(
                title=notice.title,
                description=notice.description,
                location=notice.location,
                buyer=notice.buyer,
                volume=notice.volume,
                publication_deadline=notice.publication_deadline,
                submission_deadline=notice.submission_deadline
            )

            self.analyzer.database.add(notice_entity)
            self.analyzer.database.commit()

            if related_ids is not None:
                for category_id in related_ids.categoryIds:
                    notice_category = NoticeCategory(notice_id=notice_entity.id, category_id=category_id)
                    notice_entity.categories.append(notice_category)
                    self.analyzer.database.add(notice_category)
                    self.analyzer.database.commit()

                for location_id in related_ids.locationIds:
                    notice_location = NoticeLocation(notice_id=notice_entity.id, location_id=location_id)
                    notice_entity.locations.append(notice_location)
                    self.analyzer.database.add(notice_location)
                    self.analyzer.database.commit()

            notice_entities.append(notice_entity)

        return notice_entities
