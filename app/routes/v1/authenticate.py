from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from datetime import datetime
from decouple import config

from dependencies.oauth2 import create_access_token, authenticate_user, create_refresh_token

authenticate = APIRouter(prefix=['/application/version/v1/routes/authenticate'], tags=['Authenticate'])

@authenticate.post("/login", status_code=status.HTTP_200_OK)
async def login_auth(response: Response, login_form: OAuth2PasswordRequestForm):
    get_usr = {"username": login_form.username, "password": login_form.password}
    user = await authenticate_user(get_usr)
    if not user:
        return False
    access_token = await create_access_token(token_dict={"sub": user.username}, expires_delta=config("ACCESS_TOKEN_VOID"))

    response.set_cookie(key="access_token", value=access_token, path="/", expires=str(config("ACCESS_TOKEN_VOID"), httponly=False))
    return JSONResponse(content={"access_token": access_token})