from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.utils import decode_jwt
from src.database import get_db

security = HTTPBearer()


async def get_current_user(
        db: AsyncSession = Depends(get_db),
        credentials = Depends(security)
):
    token = credentials.credentials
    payload = await decode_jwt(token)

    if not payload or 'sub' not in payload:
        raise HTTPException(status_code=401, detail='Invalid or expired token')

    res = await db.execute(select(User).where(User.username == payload['sub']))

    user = res.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail='User not found')


    return user




