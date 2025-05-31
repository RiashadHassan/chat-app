import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI

from app.user.api import user

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)


app = FastAPI()


@app.get("/")
def health_check():
    return {"Status": "Welcome to the Chat Service!"}


app.include_router(user.router, prefix="/users")
