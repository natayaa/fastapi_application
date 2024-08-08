import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, BINARY
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

    user_detail = relationship("TBUserDetails", back_populates="user_acc", uselist=False)

class TBUserDetails(Base):
    __tablename__ = "tb_user_detail"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    middlename = Column(String)
    lastname = Column(String)
    address_1 = Column(String)
    address_2  = Column(String)
    address_3 = Column(String)
    bank_id = Column(Integer, nullable=False)
    linked_profile = Column(String)
    avatar = Column(BINARY)
    bank_name = Column(String)
    total_login_time = Column(Integer)
    user_id = Column(Integer, ForeignKey("tb_users.id"))

    user_acc = relationship("TBUsers", back_populates="user_detail")