from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from decouple import config

import pytz

from database.transactions.tb_users_trans import UsersTransaction

# import hashing verificator
from dependencies.critical_Includes.security_inspection import verify_password

oauth2_route_scheme = OAuth2PasswordBearer(tokenUrl=config("OAUTH2_URL_LINK"))


# begin data transaction 
uConn = UsersTransaction()

async def verify_token(token_data: str):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credential.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        secret_key = config("OAUTH2_SECRET_KEY")
        algorithm = config("OAUTH2_ALGORITHM")
        # Decode the token and verify claims
        payload = jwt.decode(token_data, secret_key, algorithms=[algorithm])
        # Extract the username\
        username: str = payload.get("sub")
        if not username:
            raise cred_exception

        # Check token expiration
        exp = payload.get("exp")
        if exp:
            now = datetime.now().timestamp()  # Use utcnow for consistency
            if now > exp:
                # Token is expired, generate a new access token
                new_access_token = await create_access_token(payload)
                return new_access_token

        # Return username if everything is valid
        return username

    except JWTError as jwte:
        # Handle JWT errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"JWT Error: {str(jwte)}"
        )
    except Exception as e:
        # Handle other potential exceptions
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authorization error: {str(e)}"
        )


async def get_current_user(token: Annotated[str, Depends(oauth2_route_scheme)]):
    """
    JWT Verification (use to compile token name)
    decoding JWT into separated pieces
    """
    try:
        username = await verify_token(token_data=token)
        get_user = uConn.get_user(username=username)
        if not get_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not validate credential"
            )
        return get_user
    except Exception as e:
        # Missing JWT or Corrupted/Missing Subject to be authorized
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Something missing somewhere else, try another authentication"
        )



async def create_access_token(data: dict):
    to_encode = data.copy()
    # Ensure the expiry time is 15 minutes
    expire = datetime.now() + timedelta(minutes=int(config("OAUTH2_TOKEN_EXPIRES")))
    #print(f"Expiration time (UTC): {expire}")

    to_encode.update({"exp": expire})
    #print(to_encode.get("exp"))
    secret_key = config("OAUTH2_SECRET_KEY")
    algorithm = config("OAUTH2_ALGORITHM")
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def authenticate_user(**userPayload):
    # verify
    user = uConn.get_user(username=userPayload.get("username"))
    if not user:
        return False
    
    if not verify_password(input_password=userPayload.get("password"), hashed_password=user.password):
        return False
    
    return user


