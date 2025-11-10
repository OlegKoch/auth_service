from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.auth.models import User
from src.auth.utils import hash_password, verify_password, create_jwt_token
from src.auth.schemas import RegisterIn, UserOut, LoginIn
from src.database import get_db

router = APIRouter(prefix='api/v1/auth', tags=['auth'])

@router.post("/register", response_model=UserOut)
async def register(
        payload: RegisterIn,
        db: AsyncSession = Depends(get_db)
):
    user = User(
        username=payload.username,
        pass_hash=hash_password(payload.password),
        info=payload.info
    )

    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Username already taken")

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    await db.refresh(user)
    return user


@router.post("/login", response_model=UserOut)
async def login(
        payload: LoginIn,
        db: AsyncSession = Depends(get_db)
):
    try:
        res = await db.execute(select(User).where(User.username == payload.username))
        user = res.scalar_one_or_none()

        if not user:
            raise ValueError("User not found")

        if not verify_password(payload.password, user.pass_hash):
            raise ValueError("Invalid password")

        token = create_jwt_token(sub=user.username)

        return {"access_token": token, "token_type": "bearer"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


