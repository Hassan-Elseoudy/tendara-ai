from typing import List

from sqlalchemy import select, and_
from sqlalchemy.orm import Session, selectinload
from sqlmodel import select

from tendara_ai_challenge.matching.entity import Profile, Notice, NoticeCategory, NoticeLocation


def find_relevant_notices(profile: Profile, db: Session) -> List[Notice]:
    """Given the company's search profile and all notices, returns only the relevant notices for the company."""
    profile_tags_set = set(tag.lower() for tag in profile.tags.split(", ")) if profile.tags else set()

    # Define the query to filter notices based on Profile's category, location, and tags
    statement = (
        select(Notice)
        .join(NoticeLocation, NoticeLocation.notice_id == Notice.id)
        .join(NoticeCategory, NoticeCategory.notice_id == Notice.id)
        .where(
            and_(
                NoticeCategory.category_id == profile.category_id,
                NoticeLocation.location_id == profile.location_id
            )
        )
        .options(selectinload(Notice.categories), selectinload(Notice.locations))
    )

    # Execute the query
    relevant_notices = db.exec(statement).all()

    # Filter and sort notices based on tag overlap in description
    filtered_notices = [
        (notice, sum(1 for word in notice.description.lower().split() if word in profile_tags_set))
        for notice in relevant_notices
    ]

    # Sort by match count in descending order
    sorted_notices = [notice for notice, match_count in sorted(filtered_notices, key=lambda x: x[1], reverse=True)]

    return sorted_notices
