from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from db import get_session
from services.kompetenz_service import KompetenzService
from models.kompetenz import Kompetenz

router = APIRouter(prefix="/kompetenzen", tags=["Kompetenzen"])


@router.get("/")
async def alle(session: AsyncSession = Depends(get_session)):
    return await KompetenzService.alle(session)


@router.get("/{kompetenz_id}")
async def detail(kompetenz_id: int, session: AsyncSession = Depends(get_session)):
    k = await KompetenzService.finde(session, kompetenz_id)
    if not k:
        raise HTTPException(404, "Kompetenz nicht gefunden")
    return k


@router.get("/suche/{text}")
async def suche(text: str, session: AsyncSession = Depends(get_session)):
    return await KompetenzService.suche(session, text)


@router.post("/")
async def erstellen(daten: Kompetenz, session: AsyncSession = Depends(get_session)):
    return await KompetenzService.erstelle(session, daten)
