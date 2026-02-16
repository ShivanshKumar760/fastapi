from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String,Text

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/pythontestdb"

engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # same as hikari default
    max_overflow=0,      # don't allow extra
    pool_timeout=30,     # wait time if pool full
    pool_recycle=1800    # recycle connections every 30 minutes
)
# create_engine is thread-safe and will manage the connection pool for us like hikari does. 
# It will ensure that multiple threads can safely acquire and release connections without conflicts or data corruption. The connection pool will handle the allocation of connections to threads, ensuring that they are used efficiently and safely.
# what does thread safe mean : Multiple threads can use the same 
# resource at the same time without causing data corruption, crashes, or unpredictable behavior.

#engine → Knows how to talk to the database. Basically the "database connection manager". 
# It manages a pool of connections to the database and provides a way to 
# execute SQL statements and manage transactions. Like on what protocol to use, how to handle connections, etc.


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
#Session → Actually talks to the database.
#It is the main interface for interacting with the database.

Base = declarative_base()
#Base → Base class for our models. Models → Represent tables.


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("Database and tables created successfully.")