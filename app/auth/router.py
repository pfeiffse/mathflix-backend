from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from db import get_session
from pydantic import BaseModel
from models.user import User
from auth.security import hash_password, verify_password, create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])


class RegisterModel(BaseModel):
    email: str
    password: str


class LoginModel(BaseModel):
    email: str
    password: str


class RefreshModel(BaseModel):
    refresh_token: str


@router.post("/register")
async def register(data: RegisterModel, session: AsyncSession = Depends(get_session)):
    res = await session.exec(select(User).where(User.email == data.email))
    if res.first():
        raise HTTPException(400, "E-Mail bereits vergeben")

    u = User(email=data.email, password_hash=hash_password(data.password))
    session.add(u)
    await session.commit()
    await session.refresh(u)

    return {"message": "Benutzer registriert", "user_id": u.id}


@router.post("/login")
async def login(data: LoginModel, session: AsyncSession = Depends(get_session)):
    res = await session.exec(select(User).where(User.email == data.email))
    u = res.first()

    if not u or not verify_password(data.password, u.password_hash):
        raise HTTPException(401, "Login fehlgeschlagen")

    return {
        "access": create_access_token(u.id, u.role),
        "refresh": create_refresh_token(u.id)
    }


@router.post("/refresh")
async def refresh_token(data: RefreshModel):
    try:
        payload = jwt.decode(
            data.refresh_token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGO]
        )

        if payload.get("type") != "refresh":
            raise Exception()

        new_token = create_access_token(payload["sub"], "teacher")
        return {"access": new_token}

    except:
        raise HTTPException(401, "Ungültiger Refresh Token")