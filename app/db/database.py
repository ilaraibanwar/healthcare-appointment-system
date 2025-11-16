# app/db/database.py
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # loads .env from project root if present

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # fallback for quick local development
    print(
        "WARNING: DATABASE_URL not set — falling back to SQLite ./dev.db. "
        "Set DATABASE_URL in your .env to use PostgreSQL.",
        file=sys.stderr,
    )
    DATABASE_URL = "sqlite:///./dev.db"
    # For SQLite, ensure connect args for multithreading with SQLAlchemy
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
