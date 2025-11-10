from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import src.config as config

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str) -> str:
    return pwd.hash(password)


async def verify_password(plan: str, hashed: str) -> bool:
    return pwd.verify(plan, hashed)


async def create_jwt_token(sub: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(config.ACCESS_TOKEN_MIN)
    payload = {"sub": sub, "exp": expire}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALG)


async def decode_jwt(token: str) -> dict | None:
    return jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALG])


