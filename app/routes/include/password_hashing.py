from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import bcrypt

# init argon
pwHasher = PasswordHasher(hash_len=64, salt_len=8)

def hash_password(plain_password: str, salt: bytes) -> str:
    hashed_password = bcrypt.hashpw(plain_password.encode("UTF-8"), salt)

    return hashed_password

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("UTF-8"), hashed_password.encode("UTF-8"))


def argon_hash(plain_password: str) -> str:
    return pwHasher.hash(plain_password)

def verify_argon(password: str, hashed_password: str) -> bool:
    try:
        pwHasher.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False
    
