from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from database import Base,engine 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String,unique=True,index=True)
    password = Column(String)

    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")

Base.metadata.create_all(bind=engine)