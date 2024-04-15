from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .base import Base
from .seed import seed_charging_station_types
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    try:
        logger.info("Creating all tables in the database if needed...")
        Base.metadata.create_all(bind=engine)
        logger.info("Success.")

        with Session(engine) as session:
            logger.info("Seeding initial data into the database if needed...")
            seed_charging_station_types(session)
            logger.info("Success.")
    except Exception as e:
        logger.error("Failed to initialize the database.")
        raise RuntimeError("Database initialization failed") from e


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
