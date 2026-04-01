from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.baustein import Baustein
from models.baustein_kompetenz import BausteinKompetenz


class BausteinService:

    @staticmethod
    async def alle(session: AsyncSession):
        result = await session.exec(select(Baustein))
        return result.all()

    @staticmethod
    async def finde(session: AsyncSession, baustein_id: int):
        return await session.get(Baustein, baustein_id)

    @staticmethod
    async def nach_kompetenz(session: AsyncSession, kompetenz_id: int):
        statement = (
            select(Baustein)
            .join(BausteinKompetenz)
            .where(BausteinKompetenz.kompetenz_id == kompetenz_id)
        )
        result = await session.exec(statement)
        return result.all()

    @staticmethod
    async def erstelle(session: AsyncSession, daten: Baustein, kompetenzen: list[int]):
        session.add(daten)
        await session.commit()
        await session.refresh(daten)

        # Mapping hinzufügen
        for k in kompetenzen:
            link = BausteinKompetenz(baustein_id=daten.id, kompetenz_id=k)
            session.add(link)

        await session.commit()
        return daten

    @staticmethod
    async def aktualisiere(session: AsyncSession, baustein: Baustein, daten: dict):
        for key, val in daten.items():
            setattr(baustein, key, val)
        await session.commit()
        await session.refresh(baustein)
        return baustein

    @staticmethod
    async def loeschen(session: AsyncSession, baustein_id: int):
        b = await session.get(Baustein, baustein_id)
        if b:
            await session.delete(b)
            await session.commit()
        return True