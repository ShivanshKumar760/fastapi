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



SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), unique=True, nullable=False)

Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("Database and tables created successfully.")