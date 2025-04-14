from app.database.models import async_session
from app.database.models import VPNCategory
from sqlalchemy import select


async def set_vpn_category(name):
    async with async_session() as session:
        category = await session.scalar(select(VPNCategory).where(VPNCategory.name == name))

        if not category:
            session.add(VPNCategory(name=name))
            await session.commit()