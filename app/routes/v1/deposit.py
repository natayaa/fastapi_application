from fastapi import APIRouter, status, Request, Depends, HTTPException
from fastapi.responses import JSONResponse

from database.transactions.tb_depositor import DepositorClient
from models.depositor_client import AddNewClient

from datetime import datetime

from dependencies.oauth2 import get_current_user


deposit_client = APIRouter(prefix="/application/version/v1/clients/deposit", tags=["Depositor Client"])
clients = DepositorClient()

@deposit_client.get("/get_client")
async def get_client(request: Request, authorization: str = Depends(get_current_user),
                     limit: int = 10, offset: int = 0):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No Authorization can be read")
    
    list_client = clients.get_client_info(limit=limit, offset=offset)
    return list_client
    

@deposit_client.post("/add_client_new")
async def add_client(request: Request, add_new_client: AddNewClient, authorization: str = Depends(get_current_user)):
    datetime_formatted_now = datetime.now().strftime("%Y-%m-%d, %H:%M")
    payload = {"client_name": add_new_client.client_name, "client_loan_amount": add_new_client.client_loan_amount,
               "client_debt_date": datetime_formatted_now, "client_phone_number": add_new_client.client_phone_number,
               "client_email": add_new_client.client_email, "client_assurance": add_new_client.client_assurance,
               "client_due_date": add_new_client.client_due_date}
    client = clients.register_client(**payload)
    if client:
        return JSONResponse(content={"message": f"CLient with name : {add_new_client.client_name} being registered into the system."})
    else:
        raise HTTPException(detail="an error occured", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)