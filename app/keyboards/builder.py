from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.vpn_categories.select import get_vpn_categories


async def user_vpn_categories():
    kb = InlineKeyboardBuilder()

    categories = await get_vpn_categories()

    for category in categories:
        kb.row(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))

    return kb.as_markup()