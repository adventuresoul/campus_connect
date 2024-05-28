from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load all the environment variables
load_dotenv()
user_name = os.getenv("name")
password = os.getenv("password")
ip = os.getenv("ip")
db = os.getenv("db")

# Correct the DATABASE_URL
DATABASE_URL = f"postgresql://{user_name}:{password}@{ip}/{db}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
