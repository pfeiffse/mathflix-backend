from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from core.settings import settings
from db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from models.user import User

security = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO])

        if payload.get("type") != "access":
            raise HTTPException(401, "Ungültiger Token-Typ")

        user = await session.get(User, payload["sub"])
        if not user:
            raise HTTPException(404, "Benutzer nicht gefunden")

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültiger Token"
        )


def requires_role(*roles):
    def wrapper(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(403, "Zugriff verweigert")
        return user
    return wrapper