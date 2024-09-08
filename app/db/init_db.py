from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base
from config.config import environments

engine = create_engine(environments['database']['url'])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
