from database import password_hasher
from schemas import UserInDB
from database import fake_database


def verify_password(user_password, user_hashed_password):
    return password_hasher.verify(user_password, user_hashed_password)


def get_user(username: str):
    if username in fake_database.keys():
        return UserInDB(**fake_database[username])
    return None


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
