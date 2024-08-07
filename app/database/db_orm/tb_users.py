import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database.dbconn import Base

class TBUsers(Base):
    __tablename__ = "tb_users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    security_code = Column(Integer)
    phone_number = Column(String)
    phone_number_bak = Column(String)
    level = Column(Integer, default=100)