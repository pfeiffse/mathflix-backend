from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.stundenplan import Stundenplan


class StundenplanService:

    @staticmethod
    async def speichern(session: AsyncSession, plan: Stundenplan):
        session.add(plan)
        await session.commit()
        await session.refresh(plan)
        return plan

    @staticmethod
    async def finde(session: AsyncSession, plan_id: int):
        return await session.get(Stundenplan, plan_id)

    @staticmethod
    async def alle(session: AsyncSession):
        result