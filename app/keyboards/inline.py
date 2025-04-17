from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import CHANNEL_LINK

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Текст 1", callback_data="text_1")],
    ]
)

user_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Купить VPN", callback_data="buy")],
        [InlineKeyboardButton(text="Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="Поддержка", url="https://t.me/psych0ce00")]
    ]
)

check_sub = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="Проверить подписку", callback_data="check_sub")]
    ]
)
