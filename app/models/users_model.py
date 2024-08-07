from pydantic import BaseModel
from pydantic import EmailStr, Field, field_validator
from typing_extensions import Dict

import re

class RegisterUserModel(BaseModel):
    username: str = Field(..., min_length=6, max_length=20)
    password: str = Field(..., min_length=8, max_length=64)
    email: EmailStr
    security_code: int = Field(..., ge=6)
    phone_number: str = Field(..., min_length=13, max_length=20)
    phone_number_bak: str = Field(..., min_length=12, max_length=20)

    @field_validator("password")
    def validate_password(cls, value):
        # Regex to allow alphanumeric characters and selected special characters
        pattern = re.compile(r'^[a-zA-Z0-9!@#$%^&*()\-_=+\[\]{};:\'",.<>/?\\|]+$')
        if not pattern.match(value):
            raise ValueError("Password contains invalid characters")
        
        return value
    
    @field_validator("email")
    def validate_email(cls, value):
        pattern = re.compile(r'^[a-zA-Z0-9_.+.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-0-.]+$')

        # check if the email matches the pattern
        if not pattern.match(value):
            raise ValueError("Invalid email address")
        
        return value
    
    class Config:
        arbitrary_types_allowed = False
    

class retvalRegister(BaseModel):
    username: str 
    email: str

class RegisterResponse(BaseModel):
    status_code: int
    message: str
    data: retvalRegister