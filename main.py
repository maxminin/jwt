from fastapi import FastAPI
from routers import accounts_router

app = FastAPI()

app.include_router(accounts_router)
