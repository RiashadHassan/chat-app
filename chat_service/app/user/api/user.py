from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.read import User
from app.db.dependency import get_db
from app.user.schema import UserOut

router = APIRouter()


@router.get("/", response_model=list[UserOut])
async def user_list_api(db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.is_deleted == False)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{uid}", response_model=UserOut)
async def user_details_api(uid: UUID, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.uid == uid)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return UserOut.model_validate(user)
