from datetime import datetime
from typing import List

from pydantic import BaseModel

from tendara_ai_challenge.matching.entity import Notice


class NoticeModel(BaseModel):
    """A tender notice published on a procurement portal.
    
    Represents a public procurement notice containing details about
    the tender, including title, description, location, and deadlines.
    """

    title: str
    """One-line summary title of the tender notice."""

    description: str
    """Detailed description of the tender requirements and scope."""

    # TODO: Later on we may support geo location coordinated, or adding regions? Not only strings.
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


# TODO: Later on we can provide a feedback model
# class FeedbackModel(BaseModel):
#     feedback_id: int
#     profile_id: int
#     notice: NoticeModel
#     feedback_rating: int
#     feedback_text: str

class MatchingNoticesResponse(BaseModel):
    notices: List[Notice]

    # TODO: Later on we can add a match score to the response and present it to the user?
    # match_score: float = 0.0
