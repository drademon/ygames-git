from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from database import Base
from sqlalchemy import Column, Integer, String


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    message = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}