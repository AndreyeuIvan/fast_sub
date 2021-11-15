from passlib.context import CryptContext

pwd_content = CryptContext(schemes=['bcrypt'], deprecated ='auto')

def hash(password: str):
    return pwd_content.hash(password)

def verify(plain_pass, hashed_pass):
    return pwd_content.verify(plain_pass, hashed_pass)
