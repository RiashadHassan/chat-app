from uuid import UUID
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def user_list_api():
    return {"users": "LIST OF USERS"}

@router.get("/{uid}")
def user_details_api(uid: UUID):
    return {"users": "LIST OF USERS"}
