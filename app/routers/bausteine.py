from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel
from db import get_session
from services.baustein_service import BausteinService
from models.baustein import Baustein

router = APIRouter(prefix="/bausteine", tags=["Bausteine"])


class BausteinCreate(BaseModel):
    titel: str
    beschreibung: str | None = None
    einstieg: str | None = None
    erarbeitung: str | None = None
    sicherung: str | None = None
    reflexion: str | None = None
    tags: str | None = None
    kompetenzen: list[int]


@router.post("/")
async def erstellen(daten: BausteinCreate, session: AsyncSession = Depends(get_session)):
    b = Baustein(
        titel=daten.titel,
        beschreibung=daten.beschreibung,
        einstieg=daten.einstieg,
        erarbeitung=daten.erarbeitung,
        sicherung=daten.sicherung,
        reflexion=daten.reflexion,
        tags=daten.tags
    )
    return await BausteinService.erstelle(session, b, daten.kompetenzen)


@router.get("/")
async def alle(session: AsyncSession = Depends(get_session)):
    return await BausteinService.alle(session)


@router.get("/kompetenz/{kid}")
async def nach_kompetenz(kid: int, session: AsyncSession = Depends(get_session)):
    return await BausteinService.nach_kompetenz(session, kid)