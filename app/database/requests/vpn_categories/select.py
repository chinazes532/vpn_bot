from app.database.models import async_session
from app.database.models import VPNCategory
from sqlalchemy import select


async def get_vpn_categories():
    async with async_session() as session:
        categories = await session.scalars(select(VPNCategory))
        return categories



