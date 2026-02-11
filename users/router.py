from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from core.db import get_db

from . import schemas, service
from .models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserRead)
async def create_user(
    user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)
) -> schemas.UserRead:
    existing_user = await service.get_user_by_email(db, email=user_in.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await service.create_user(db, user_in)
    return user


@router.get("/me", response_model=schemas.UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    """
    This just returns the current user by token,
    but it's a good example of how to use the get_current_user dependency.
    """
    return current_user
