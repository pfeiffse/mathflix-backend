from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.material import Material


class MaterialService:

    @staticmethod
    async def alle(session: AsyncSession):
        result = await session.exec(select(Material))
        return result.all()

    @staticmethod
    async def finde(session: AsyncSession, material_id: int):
        return await session.get(Material, material_id)

    @staticmethod
    async def speichern(session: AsyncSession, material: Material):
        session.add(material)
        await session.commit()
        await session.refresh(material)
        return material

    @staticmethod
    async def update(session: AsyncSession, material: Material, daten: dict):
        for key, value in daten.items():
            setattr(material, key, value)
        await session.commit()
        await session.refresh(material)
        return material