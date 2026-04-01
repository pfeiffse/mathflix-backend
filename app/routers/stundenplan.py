from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel
from sqlmodel import select
from db import get_session
from core.eventbus import EventBus
from services.stundenplan_service import StundenplanService
from services.kompetenz_service import KompetenzService
from agents.stundenplan_agent import StundenplanAgent
from models.stundenplan import Stundenplan
from models.baustein import Baustein
from models.lehrbuch import LehrbuchSeite

router = APIRouter(prefix="/stundenplan", tags=["Stundenplan"])


class StundenplanRequest(BaseModel):
    kompetenz_id: int
    dauer_min: int = 45


@router.post("/generate")
async def generate(req: StundenplanRequest, session: AsyncSession = Depends(get_session)):

    kompetenz = await KompetenzService.finde(session, req.kompetenz_id)

    b_stmt = select(Baustein).where(Baustein.kompetenz_id == req.kompetenz_id)
    bausteine = (await session.exec(b_stmt)).all()

    lehrbuch = (await session.exec(select(LehrbuchSeite))).all()

    data = StundenplanAgent.generiere_plan(
        kompetenz.titel,
        bausteine,
        lehrbuch,
        req.dauer_min
    )

    sp = Stundenplan(
        titel=f"Stunde zu {kompetenz.titel}",
        kompetenz_id=req.kompetenz_id,
        dauer_min=req.dauer_min,
        plan_json=json.dumps(data, ensure_ascii=False)
    )

    saved = await StundenplanService.speichern(session, sp)
    return saved


@router.get("/")
async def alle(session: AsyncSession = Depends(get_session)):
    return await StundenplanService.alle(session)


@router.get("/{plan_id}")
async def detail(plan_id: int, session: AsyncSession = Depends(get_session)):
    return await StundenplanService.finde(session, plan_id)