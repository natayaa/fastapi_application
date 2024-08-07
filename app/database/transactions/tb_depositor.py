from sqlalchemy import or_
from sqlalchemy.exc import NoResultFound

from database.db_orm.tb_depositor import TBDepositor as client_depo
from database.dbconn import DBConnection

class DepositorClient(DBConnection):
    def __init__(self):
        super().__init__()

    def get_client_info(self, limit: int, offset: int):
        query = self.session.query(client_depo).offset(offset).limit(limit).all()
        return query
    
    def register_client(self, **client_payload):
        client = client_depo(debt_name=client_payload.get("client_name"),
                             debt_amount=client_payload.get("client_loan_amount"),
                             debt_date=client_payload.get("client_debt_date"),
                             debt_phone_number=client_payload.get("client_phone_number"),
                             debt_email=client_payload.get("client_email"),
                             debt_assurance=client_payload.get("client_assurance"),
                             debt_due_date=client_payload.get("client_due_date"))
        self.session.add(client)
        self.session.commit()
        return True
    
    def update_client_debt_history(self, debt_name: str, new_amount: int, new_status: bool):
        query = self.session.query(client_depo).filter_by(debt_name = debt_name).first()
        try:
            if query:
                query.debt_amount = new_amount
                query.debt_status = new_status
                self.session.commit()
                return True
            else:
                return False
        except NoResultFound:
            return False
        except Exception as e:
            self.session.rollback()
            return False