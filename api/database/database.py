from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .base import Base
from .seed import seed_charging_station_types
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        seed_charging_station_types(session)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
