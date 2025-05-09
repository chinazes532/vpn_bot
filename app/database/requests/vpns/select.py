from app.database.models import async_session
from app.database.models import VPN
from sqlalchemy import select


async def get_vpn_by_category_id(category_id):
    async with async_session() as session:
        vpns = await session.scalars(select(VPN).where(VPN.category_id == category_id))
        return vpns


async def get_vpn_by_id(vpn_id):
    async with async_session() as session:
        vpn = await session.scalar(select(VPN).where(VPN.id == vpn_id))
        return vpn
