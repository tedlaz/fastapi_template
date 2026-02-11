from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_token, verify_hash
from users.schemas import UserRead
from users.service import get_user_by_email


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> UserRead | None:
    user = await get_user_by_email(db, email=email)

    if not user:
        return None

    verified, updated_hash = verify_hash(password, user.hashed_password)

    if not verified:
        return None

    if updated_hash:
        user.hashed_password = updated_hash
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user


async def login_for_access_token(
    db: AsyncSession, email: str, password: str
) -> str | None:
    user = await authenticate_user(db, email, password)

    if not user:
        return None

    return create_token(user.email)
