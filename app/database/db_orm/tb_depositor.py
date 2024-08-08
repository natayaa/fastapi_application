from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean 

from database.dbconn import Base

class TBDepositor(Base):
    __tablename__ = "tb_depositor"

    debt_id = Column(Integer, autoincrement=True, primary_key=True)
    debt_name = Column(String)
    debt_amount = Column(Integer, default=0)
    debt_amount_left = Column(Integer, default=0)
    debt_date = Column(String, default=datetime.now())
    debt_phone_number = Column(String)
    debt_email = Column(String)
    debt_assurance = Column(String)
    debt_status = Column(Boolean, default=False)
    debt_due_date = Column(String)