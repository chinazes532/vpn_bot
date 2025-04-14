from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.vpn_categories.select import get_vpn_categories
from app.database.requests.vpns.select import get_vpn_by_category_id


async def user_vpn_categories():
    kb = InlineKeyboardBuilder()

    categories = await get_vpn_categories()

    for category in categories:
        kb.row(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))

    return kb.as_markup()


async def user_countries(vpn_category_id):
    kb = InlineKeyboardBuilder()

    countries = await get_vpn_by_category_id(vpn_category_id)

    for country in countries:
        kb.row(InlineKeyboardButton(text=country.name, callback_data=f"country_{country.id}"))

    return kb.as_markup()