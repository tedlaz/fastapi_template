from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_hash

from . import models, schemas


async def create_user(db: AsyncSession, user_in: schemas.UserCreate) -> models.User:
    db_user = models.User(
        email=user_in.email,
        hashed_password=create_hash(user_in.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()
