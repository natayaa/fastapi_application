from argon2 import PasswordHasher, exceptions
from decouple import config


ph = PasswordHasher(hash_len=64)

def create_hashed_pw(password: str) -> str:
    """
    Hash the password using Argon2 with salt and pepper.
    """
    return ph.hash(password=password)

def verify_password(input_password: str, hashed_password: str) -> bool:
    """
    Verify the input password against the stored hashed password.
    """
    try:
        ph.verify(hashed_password, input_password)
        return True
    except exceptions.VerifyMismatchError as mismatch:
        return False