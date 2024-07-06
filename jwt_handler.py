from datetime import datetime, timedelta
from schemas import TokenData
from fastapi import Depends, HTTPException
from services import get_user
import jwt as pyjwt
from database import SECRET_KEY, ALGORITHM, oauth2_scheme, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


def create_refresh_token(data: dict):
    data_to_encode = data.copy()
    refresh_token_expire_time = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data_to_encode.update({"exp": refresh_token_expire_time})
    encoded_jwt_refresh = pyjwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt_refresh


def create_access_token(data: dict):
    data_to_encode = data.copy()
    access_token_expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": access_token_expire_time})
    encoded_jwt_access = pyjwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt_access


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        username: str = payload.get("username")
        email: str = payload.get("email")
        if username is None or email is None:
            return None
        token_data = TokenData(username=username, email=email)
    except pyjwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user(username=token_data.username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user



