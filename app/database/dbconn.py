from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_HOST = "sqlite:///database/apl_db.db"

db_engine = create_engine(url=SQL_HOST, echo=False)
Base = declarative_base()
SessionLocale = sessionmaker(autoflush=False, autocommit=False, bind=db_engine)

class DBConnection:
    def __init__(self):
        self.session = SessionLocale()