from sqlalchemy import or_

from database.db_orm.tb_users import TBUsers, TBUserDetails
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
        
    def get_detail_user(self, username: str):
        getUser = self.get_user(username=username)
        user_detail = self.session.query(TBUserDetails).filter(TBUserDetails.user_id == getUser.id).first()
        return user_detail
        
    def edit_detail_user(self, username: str, new_details: dict):
        """
            Consist of 
            - firstname
            - middlename (optional)
            - lastname
            - address_1
            - address_2
            - address_3
            - bank_id (integer)
            - linked_profile
            - avatar (BLOB File/img)
            - bank_name
            - total_login_time = Increment
            
        """
        try:
            current_user = self.get_user(username=username)
            if not current_user:
                return False

            # Get the current user's details
            user_details = self.session.query(TBUserDetails).filter(TBUserDetails.user_id == current_user.id).first()
            if not user_details:
                return False

            # Update the details based on the new_details dictionary
            for key, value in new_details.items():
                if hasattr(user_details, key):
                    setattr(user_details, key, value)
                elif hasattr(current_user, key):
                    setattr(current_user, key, value)

            # Commit the changes to the database
            self.session.commit()
            return True
        except Exception as e:
            # Rollback in case of any error
            self.session.rollback()
            print(f"Error updating user details: {e}")
            return False

        
    def register_user(self, **payload_register):
        try:
            if self.check_existing_user(payload_register.get("username"), payload_register.get("email"), payload_register.get("phone_number")):
                return False
            
            # Hash the password using argon_hash
            password = argon_hash(payload_register.get('password'))
            
            # Create the user object
            user = TBUsers(
                username=payload_register.get("username"),
                password=password, 
                email=payload_register.get("email"),
                security_code=payload_register.get("security_code"),
                phone_number=payload_register.get("phone_number"),
                phone_number_bak=payload_register.get("phone_number_backup")
            )
            
            # Add the user to the session
            self.session.add(user)
            self.session.commit()  # Commit to get the user ID

            # Create user details object
            user_details = TBUserDetails(
                firstname=payload_register.get("firstname"),
                middlename=payload_register.get("middlename"),
                lastname=payload_register.get("lastname"),
                address_1=payload_register.get("address_1"),
                address_2=payload_register.get("address_2"),
                address_3=payload_register.get("address_3"),
                bank_id=payload_register.get("bank_id"),
                linked_profile=payload_register.get("linked_profile"),
                avatar=payload_register.get("avatar"),
                bank_name=payload_register.get("bank_name"),
                total_login_time=payload_register.get("total_login_time", 0),
                user_id=user.id  # Link the user details to the created user
            )
            
            # Add the user details to the session
            self.session.add(user_details)
            self.session.commit()
            
            return True
        except Exception as e:
            print(f"Error : {str(e)}")
            self.session.rollback()
            return False