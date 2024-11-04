from datetime import datetime
from typing import List

from pydantic import BaseModel


class NoticeModel(BaseModel):
    """A tender notice published on a procurement portal.
    
    Represents a public procurement notice containing details about
    the tender, including title, description, location, and deadlines.
    """

    title: str
    """One-line summary title of the tender notice."""

    description: str
    """Detailed description of the tender requirements and scope."""

    location: str
    """Geographic location where services will be provided (country/city)."""

    buyer: str
    """Name of the public institution issuing the tender."""

    volume: int
    """Estimated contract value in EUR (non-negative integer)."""

    cpv_codes: List[str]
    """Common Procurement Vocabulary (CPV) codes identifying service types.
    
    Example:
        ["72000000-5"] for "IT services: consulting, software development, Internet, and support"
    """

    publication_deadline: datetime
    """Date and time when the notice was published."""

    submission_deadline: datetime
    """Date and time for the deadline for submitting tender proposals."""


class CategoryModel(BaseModel):
    category_id: int
    category_name: str


class NoticeCategoryModel(BaseModel):
    notice_id: int
    category_id: int
