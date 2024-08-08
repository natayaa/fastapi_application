from datetime import datetime
from sqlalchemy import Column, String, Integer

import uuid

from database.dbconn import Base


class TBTransactions(Base):
    __tablename__ = "tb_transactions"

    trans_id = Column(Integer, primary_key=True, autoincrement=True)
    uid_transaction = Column(Integer, default=uuid.uuid4())
    depositor_name = Column(String)
    deposit_amount = Column(Integer)
    date_transaction = Column(String, default=datetime.now())