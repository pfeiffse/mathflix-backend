from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.lehrbuch import LehrbuchSeite
from models.lehrbuch_kompetenz import LehrbuchKompetenz


class LehrbuchService:

    @staticmethod
    async def alle(session: AsyncSession):
        result = await session.exec(select(LehrbuchSeite))
        return result.all()

    @staticmethod
    async def finde(session: AsyncSession, seite_id: int):
        return await session.get(LehrbuchSeite, seite_id)

    @staticmethod
    async def erstelle(session: AsyncSession, seite: LehrbuchSeite, kompetenzen: list[int]):
        session.add(seite)
        await session.commit()
        await session.refresh(seite)

        # Kompetenzen verknüpfen
        for k in kompetenzen:
            link = LehrbuchKompetenz(lehrbuchseite_id=seite.id, kompetenz_id=k)
            session.add(link)

        await session.commit()
        return seite

    @staticmethod
    async def aktualisiere(session: AsyncSession, seite: LehrbuchSeite, daten: dict):
        for key, value in daten.items():
            setattr(seite, key, value)
        await session.commit()
        await session.refresh(seite)
        return seite

    @staticmethod
    async def nach_band(session: AsyncSession, band: str):
        result = await session.exec(select(LehrbuchSeite).where(LehrbuchSeite.band == band))
        return result.all()