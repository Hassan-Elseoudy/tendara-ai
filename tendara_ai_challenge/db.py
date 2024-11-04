from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from tendara_ai_challenge.matching.alchemy import Base


class Database:
    def __init__(self, db_url: str = 'sqlite:///:memory:'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self) -> Session:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
