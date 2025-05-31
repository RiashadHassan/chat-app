from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession


from .session import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        async with session.begin():  # starts a transaction, rollsback automatically incase of errors
            yield session
