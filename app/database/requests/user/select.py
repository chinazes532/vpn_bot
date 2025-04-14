from datetime import datetime

from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, func


async def get_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user


async def get_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users


async def get_users_count():
    async with async_session() as session:
        count = await session.scalar(select(func.count()).select_from(User))
        return count


async def get_statistics():
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    today_str = today.strftime('%d.%m.%Y')
    print(today_str)
    start_of_month_str = start_of_month.strftime('%d.%m.%Y')

    async with async_session() as session:
        daily_users = await session.scalar(select(func.count()).select_from(User).where(User.date == today_str))
        monthly_users = await session.scalar(select(func.count()).select_from(User).where(User.date >= start_of_month_str))
        total_users = await session.scalar(select(func.count()).select_from(User))

        return daily_users, monthly_users, total_users