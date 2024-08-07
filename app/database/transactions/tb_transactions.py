from sqlalchemy import or_

from database.db_orm.tb_transactions import TBTransactions as trans
from database.dbconn import DBConnection


class HistoryTransactions(DBConnection):
    def __init__(self):
        super().__init___()

    def get_transactions(self, page: int, perpage: int):
        query = self.session.query(trans).offset(page).limit(perpage).all()
        return query
    
    def add_transaction(self, **transaction_payload) -> bool:
        transaction= trans(depositor_name=transaction_payload.get("depositor_name"),
                            deposit_amount=transaction_payload.get("deposit_amount"))
        self.session.add(transaction)
        self.session.commit()

        return True
    
    def delete_transaction(self, id: int) -> bool:
        if not id:
            return False
        
        query = self.session.query(trans).filter_by(id=id)
        self.session.delete(query)
        self.session.commit()
        return True