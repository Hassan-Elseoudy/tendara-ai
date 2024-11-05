from datetime import date
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, create_engine, Session


class Notice(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    buyer: Optional[str] = Field(default=None)
    volume: Optional[int] = Field(default=None)
    publication_deadline: Optional[date] = Field(default=None)
    submission_deadline: Optional[date] = Field(default=None)

    categories: List["NoticeCategory"] = Relationship(back_populates="notice")
    locations: List["NoticeLocation"] = Relationship(back_populates="notice")

    def __repr__(self):
        return (
            f"<Notice(title={self.title}, description={self.description}, "
            f"buyer={self.buyer}, volume={self.volume}, "
            f"publication_deadline={self.publication_deadline}, submission_deadline={self.submission_deadline})>"
        )


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

    notices: List["NoticeCategory"] = Relationship(back_populates="category")

    def __repr__(self):
        return f"<Category(name={self.name}, id={self.id})>"


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    city: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)

    notices: List["NoticeLocation"] = Relationship(back_populates="location")

    def __repr__(self):
        return f"<Location(city={self.city}, country={self.country})>"


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: Optional[int] = Field(default=None)
    location_id: Optional[int] = Field(default=None)
    tags: Optional[str] = Field(default=None)  # TODO: A better way to store tags.
    publication_deadline: Optional[date] = Field(default=None)  # TODO: Really use publication_deadline

    # feedbacks: List["Feedback"] = Relationship(back_populates="profile")

    def __repr__(self):
        return (
            f"<Profile(id={self.id}, category_id={self.category_id}, "
            f"location_id={self.location_id}, publication_deadline={self.publication_deadline})>"
        )


# class Feedback(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     profile_id: Optional[int] = Field(default=None, foreign_key="profile.id")
#     notice_id: Optional[int] = Field(default=None, foreign_key="notice.id")
#     feedback_rating: Optional[int] = Field(default=None)
#     feedback_text: Optional[str] = Field(default=None)
#
#     profile: "Profile" = Relationship(back_populates="feedbacks")
#     notice: "Notice" = Relationship(back_populates="feedbacks")
#
#     def __repr__(self):
#         return (
#             f"<Feedback(profile_id={self.profile_id}, notice_id={self.notice_id}, "
#             f"feedback_rating={self.feedback_rating}, feedback_text={self.feedback_text})>"
#         )
#

class NoticeCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    notice_id: int = Field(default=None, foreign_key="notice.id")
    category_id: int = Field(default=None, foreign_key="category.id")

    notice: "Notice" = Relationship(back_populates="categories")
    category: "Category" = Relationship(back_populates="notices")

    def __repr__(self):
        return f"<NoticeCategory(notice_id={self.notice_id}, category_id={self.category_id})>"


class NoticeLocation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    notice_id: Optional[int] = Field(default=None, foreign_key="notice.id")
    location_id: Optional[int] = Field(default=None, foreign_key="location.id")

    notice: "Notice" = Relationship(back_populates="locations")
    location: "Location" = Relationship(back_populates="notices")

    def __repr__(self):
        return f"<NoticeLocation(notice_id={self.notice_id}, location_id={self.location_id})>"


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
