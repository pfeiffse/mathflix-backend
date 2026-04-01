from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.kompetenz import Kompetenz


class KompetenzService:

    @staticmethod
    async def alle(session: AsyncSession):
        result = await session.exec(select(Kompetenz))
        return result.all()

    @staticmethod
    async def finde(session: AsyncSession, kompetenz_id: int):
        return await session.get(Kompetenz, kompetenz_id)

    @staticmethod
    async def suche(session: AsyncSession, text: str):
        statement = select(Kompetenz).where(
            Kompetenz.titel.contains(text) |
            Kompetenz.beschreibung.contains(text) |
            Kompetenz.tags.contains(text)
        )
        result = await session.exec(statement)
        return result.all()

    @staticmethod
    async def erstelle(session: AsyncSession, daten: Kompetenz):
        session.add(daten)
        await session.commit()
        await session.refresh(daten)
        return daten

    @staticmethod
    async def aktualisiere(session: AsyncSession, kompetenz: Kompetenz, daten: dict):
        for key, val in daten.items():
            setattr(kompetenz, key, val)
        await session.commit()
        await session.refresh(kompetenz)
        return kompetenz