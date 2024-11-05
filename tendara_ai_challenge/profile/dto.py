from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SearchProfileRequestSchema(BaseModel):
    # TODO: Maybe it's suitable to use libraries like Elasticsearch or Solr for searching tags.
    tags: List[str] = Field(..., min_length=1, description="Tags or Keywords to search in database")
    category_id: int = Field(..., gt=0, description="Category ID")
    location_id: int = Field(..., gt=0, description="Location ID")

    class Config:
        orm_mode = True


class SearchProfileResponseSchema(BaseModel):
    id: int = Field(..., gt=0, description="Profile ID")
    category_id: int = Field(gt=0)
    location_id: Optional[int] = Field(default=None)
    tags: List[str] = Field(..., min_length=1)
    publication_deadline: Optional[datetime] = Field(default=None)
