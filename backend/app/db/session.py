from app.core import settings
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)