from fastapi import APIRouter, status, HTTPException, Depends, Request
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse, Response, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from typing_extensions import Annotated, Optional

from decouple import config
from datetime import timedelta

import os

# load model for the user
from models.users_model import RegisterResponse, RegisterUserModel

from dependencies.oauth2 import authenticate_user, create_access_token
from dependencies.oauth2 import get_current_user

from database.transactions.tb_users_trans import UsersTransaction

# import body model
from models.users_model import UserDetailUpdate

user_section = APIRouter(prefix="/application/version/v1", tags=['Users'])
uTrans = UsersTransaction()

expires_delta_token = int(config("OAUTH2_TOKEN_EXPIRES"))

# register user
@user_section.post("/register")
async def register_userapp(register_mod: RegisterUserModel):

    pp = RegisterResponse(status_code=status.HTTP_200_OK, message="Gotcha", 
                                                 data={"username": register_mod.username,
                                                       "email": register_mod.email})
    # check if username or email already exists
    payload = {"username": register_mod.username, "password": register_mod.password, 
                                        "email": register_mod.email, "phone_number": register_mod.phone_number,
                                        "security_code": register_mod.security_code, "phone_number_backup": register_mod.phone_number_bak}
    regist_user = uTrans.register_user(**payload)
    if regist_user is False:
        return JSONResponse(content={"message": f"{register_mod.username} or {register_mod.email} exists in our data."}, status_code=status.HTTP_202_ACCEPTED)

    return JSONResponse(content=pp.model_dump())


@user_section.post("/user/auth")
async def user_auth(response: Response, user_auth: Annotated[OAuth2PasswordRequestForm, Depends()]):
    userinfo = {"username": user_auth.username, "password": user_auth.password}
    user = await authenticate_user(**userinfo)
    if not user:
        return JSONResponse(content={"message": "Failed to authenticate, please check the username or password"}, 
                            status_code=status.HTTP_401_UNAUTHORIZED)
    
    toEncode = {"sub": user.username, "role": user.level}
    access_token = await create_access_token(data=toEncode)
    #response.headers['Authorization'] = f"bearer {access_token}"
    return JSONResponse(content={"access_token": access_token})
    

@user_section.get("/user/{username}/profile/")
async def get_user_info(request: Request, username: str, authorization: str = Depends(get_current_user)):
    if username != authorization.username:
        print("false")
    user_detail = uTrans.get_detail_user(username=username)

    return {"username": request.headers, "detail": user_detail}

@user_section.put("/user/{username}/details")
def edit_detail_user(new_details: UserDetailUpdate, username: str, authorization: str = Depends(get_current_user)):
    current_user = uTrans.get_user(authorization.username)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_details = uTrans.edit_detail_user(username=authorization.username, new_details=new_details.model_dump())
    if not user_details:
        raise HTTPException(status_code=404, detail="User details not found")

    

    return {"message": "User details updated successfully"}


@user_section.put("/user/{username}/details/avatar")
async def upload_avatar(username: str = Depends(get_current_user), avatar: UploadFile = File(...)):
    if not username:
        raise HTTPException(status_code=404, detail="User not found")
    
    av  = await avatar.read()
    avtf = uTrans.update_avatar(username, av)
    return avtf