from sqlalchemy import Column , Integer , String , ForeignKey
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String , unique=True , index=True)
    password = Column(String)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer , primary_key=True , index=True)
    name = Column(String , unique=True , index=True)
    user_id = Column(Integer,ForeignKey("users.id"),unique=True) #one projects per user 