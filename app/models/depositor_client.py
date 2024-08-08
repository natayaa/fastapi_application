from pydantic import BaseModel

class AddNewClient(BaseModel):
    client_name: str = None
    client_loan_amount: int = 0
    client_debt_date: str = None
    client_phone_number: str = None
    client_email: str = None 
    client_assurance: str = None
    client_due_date: str = None