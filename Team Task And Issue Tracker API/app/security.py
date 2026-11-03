import bcrypt
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "dfonsfokrengojnapfojgn"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30

def get_password_hash(password: str):
    
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_bytes.decpde('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False
    
def create_access_token(data: dict, expires_delta: timedelta | None) -> str:
    
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encode_jwt