from typing import List

from pydantic import BaseModel


class RelatedIds(BaseModel):
    categoryIds: List[int]
    locationIds: List[int]
