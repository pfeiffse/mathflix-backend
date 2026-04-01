from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel
from db import get_session
from models.material import Material
from services.material_service import MaterialService
from core.eventbus import EventBus

router = APIRouter(prefix="/material", tags=["Material"])


class MaterialUploadModel(BaseModel):
    titel: str
    text: str


@router.post("/")
async def upload(daten: MaterialUploadModel, session: AsyncSession = Depends(get_session)):
    material = Material(titel=daten.titel, text=daten.text)
    saved = await MaterialService.speichern(session, material)

    # Pipeline starten
    await EventBus.emit("material_uploaded", saved.id)

    return {"message": "Material hochgeladen", "id": saved.id}


@router.get("/")
async def alle(session: AsyncSession = Depends(get_session)):
    return await MaterialService.alle(session)


@router.get("/{material_id}")
async def detail(material_id: int, session: AsyncSession = Depends(get_session)):
    return await MaterialService.finde(session, material_id)
