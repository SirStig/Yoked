from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database (create tables if they do not exist)
def init_db():
    try:
        from backend.models.user import User  # Import all models here
        from backend.models.session import Session as UserSession
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        raise Exception(f"Error initializing database: {e}")