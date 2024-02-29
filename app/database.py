from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from  .config import settings
# password 
from urllib.parse import quote_plus
# password = "saini@123"
password_encoded = quote_plus(settings.database_password)

DATABASE_URL = f"postgresql://{settings.database_username}:{password_encoded}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
