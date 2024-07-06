from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "4f2d6b3a8c9e5d1f7b6a4e1d2c3b5a7d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_database = {
    "Maks": {
        "username": "Maks",
        "email": "fakeemail@gmail.com",
        "hashed_password": password_hasher.hash("qwerty12345")
    },
    "Dima": {
        "username": "Dima",
        "email": "fakeemail228@gmail.com",
        "hashed_password": password_hasher.hash("qwerty12345")
    }
}
