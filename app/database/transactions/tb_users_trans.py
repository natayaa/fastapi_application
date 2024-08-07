from sqlalchemy import or_

from database.db_orm.tb_users import TBUsers
from database.dbconn import DBConnection

# hasher password
from routes.include.password_hashing import argon_hash

class UsersTransaction(DBConnection):
    def __init__(self):
        super().__init__()

    def get_user(self, username: str):
        query = self.session.query(TBUsers).filter_by(username=username).first()
        return query
    
    def check_existing_user(self, username: str, email: str, phonenumber: str):
        """
            Return True if exists
            else False
        """
        query = self.session.query(TBUsers).filter(or_(TBUsers.username == username, TBUsers.email == email, TBUsers.phone_number == phonenumber)).first()
        if query:
            return True
        else:
            return False
        
    def register_user(self, **payload_register):
        try:
            if self.check_existing_user(payload_register.get("username"), payload_register.get("email"), payload_register.get("phone_number")):
                return False
            
            # register data from the payload
            password = argon_hash(payload_register.get('password'))
            sec_code = payload_register.get("security_code")
            user = TBUsers(username=payload_register.get("username"),
                           password=password, 
                           email=payload_register.get("email"),
                           security_code=sec_code,
                           phone_number=payload_register.get("phone_number"),
                           phone_number_bak=payload_register.get("phone_number_backup"))
            
            self.session.add(user)
            self.session.commit()
        except Exception as e:
            print(f"Error : {str(e)}")
            self.session.rollback()
            return False
        
    