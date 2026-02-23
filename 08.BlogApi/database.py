from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/pythonblogdb"

# engine = create_engine(DATABASE_URL)
#or i can specify the pool size and max overflow
engine=create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base=declarative_base()