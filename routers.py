from fastapi import APIRouter, HTTPException, Depends
from schemas import User
from database import fake_database, password_hasher
from typing import Annotated, List
from fastapi.security import OAuth2PasswordRequestForm
from services import authenticate_user
from jwt_handler import create_access_token, get_new_access_token, create_refresh_token
from schemas import Token


accounts_router = APIRouter()


@accounts_router.post("/register", response_model=User)
def register_user(username, password, email):
    if username in fake_database.keys():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = password_hasher.hash(password)
    fake_database[username] = {"username": username,
                               "email": email,
                               "hashed_password": hashed_password}
    access_token = create_access_token(data={"username": username, "email": email})
    refresh_token = create_refresh_token(data={"username": username, "email": email})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer", username=username, email=email)


@accounts_router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="This user doesn't exist")
    access_token = create_access_token(data={"username": user.username, "email": user.email})
    refresh_token = create_refresh_token(data={"username": user.username, "email": user.email})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer", username=user.username, email=user.email)


@accounts_router.get("/users", response_model=List[User])
def get_users():
    users = []
    for user in fake_database.values():
        users.append(User(username=user.get("username"), email=user.get("email")))
    return users


@accounts_router.post("/refresh")
def refresh(token: str):
    get_new_access_token(token=token)
