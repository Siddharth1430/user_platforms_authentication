from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Get the database url from .env
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Create a connection to the DATABASE_URL
engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Create the database if it doesn't exist
Base.metadata.create_all(engine)


# Create a dependency injection function to get the database
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
