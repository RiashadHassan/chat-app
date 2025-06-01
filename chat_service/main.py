import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI

from app.chat.api import channel

from app.user.api import user
from app.db.scylla import setup_keyspace_and_table

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    setup_keyspace_and_table()


@app.get("/")
def health_check():
    return {"Status": "Welcome to the Chat Service!"}


app.include_router(user.router, prefix="/users")
app.include_router(channel.router, prefix="/messages")