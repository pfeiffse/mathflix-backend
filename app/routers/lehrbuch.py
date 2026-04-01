from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel
from db import get_session
from models.lehrbuch import LehrbuchSeite
from services.lehrbuch_service import LehrbuchService
from core.eventbus import EventBus

router = APIRouter(prefix="/lehrbuch", tags=["Lehrbuch"])


class LehrbuchUpload(BaseModel):
    band: str
    kapitel: str
    seite: int
    titel: str
    text: str
    kompetenzen: list[int]


@router.post("/")
async def upload_lb(daten: LehrbuchUpload, session: AsyncSession = Depends(get_session)):
    seite = LehrbuchSeite(**daten.dict(exclude={"kompetenzen"}))
    saved = await LehrbuchService.erstelle(session, seite, daten.kompetenzen)

    await EventBus.emit("lehrbuchseite_uploaded", saved.id)

    return {"message": "Lehrbuchseite gespeichert", "id": saved.id}


@router.get("/")
async def alle(session: AsyncSession = Depends(get_session)):
    return await LehrbuchService.alle(session)


@router.get("/{seite_id}")
async def detail(seite_id: int, session: AsyncSession = Depends(get_session)):
    return await LehrbuchService.finde(session, seite_id)


@router.get("/band/{band}")
async def nach_band(band: str, session: AsyncSession = Depends(get_session)):
    return await LehrbuchService.nach_band(session, band)