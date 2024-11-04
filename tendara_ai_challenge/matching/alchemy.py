import json

from sqlalchemy import Column, Integer, String, ForeignKey, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Notice(Base):
    __tablename__ = 'notice'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    location = Column(String)
    buyer = Column(String)
    volume = Column(Integer)
    publication_deadline = Column(DATE)
    submission_deadline = Column(DATE)

    def __repr__(self):
        return f"<Notice(title={self.title}, description={self.description}, location={self.location}, buyer={self.buyer}, volume={self.volume}, publication_deadline={self.publication_deadline}, submission_deadline={self.submission_deadline})>"

    categories = relationship("NoticeCategory", back_populates="notice")
    locations = relationship("NoticeLocation", back_populates="notice")


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<({self.name}, {self.id})>"

    notices = relationship("NoticeCategory", back_populates="category")


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    country = Column(String)

    def __repr__(self):
        return f"<Location(city={self.city}, country={self.country})>"

    notices = relationship("NoticeLocation", back_populates="location")


class NoticeCategory(Base):
    __tablename__ = 'notice_category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    notice_id = Column(Integer, ForeignKey('notice.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    notice = relationship("Notice", back_populates="categories")
    category = relationship("Category", back_populates="notices")

    def __repr__(self):
        return f"<NoticeCategory(notice_id={self.notice_id}, category_id={self.category_id})>"


class NoticeLocation(Base):
    __tablename__ = 'notice_location'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Added primary key
    notice_id = Column(Integer, ForeignKey('notice.id'))
    location_id = Column(Integer, ForeignKey('location.id'))

    notice = relationship("Notice", back_populates="locations")
    location = relationship("Location", back_populates="notices")

    def __repr__(self):
        return f"<NoticeLocation(notice_id={self.notice_id}, location_id={self.location_id})>"
