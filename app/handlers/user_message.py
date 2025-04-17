import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.filters.admin_filter import AdminProtect

from app.database.requests.user.add import set_user
from app.database.requests.vpns.select import get_vpn_by_id

from app.outline_vpn.outline_vpn import OutlineVPN
from app.payments.ukassa import create_payment_one

user = Router()


@user.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery):
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    
    await callback.message.edit_text("Спасибо за подписку, вы можете пользоваться ботом!")

    await set_user(callback.from_user.id, callback.from_user.full_name, current_date)


@user.message(CommandStart())
async def start_command(message: Message):
    admin = AdminProtect()
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    if not await admin(message):  
        await message.answer(f"""🌐 <b>Добро пожаловать!</b> 🌐

Мы рады видеть вас здесь! 
Если вы ищете надежный способ обеспечить свою онлайн-безопасность и конфиденциальность, вы попали по адресу.""",
                             reply_markup=ikb.user_panel)
        await set_user(message.from_user.id, message.from_user.full_name, current_date)
    else:
        await message.answer(f"""🌐 <b>Добро пожаловать!</b> 🌐

Мы рады видеть вас здесь! 
Если вы ищете надежный способ обеспечить свою онлайн-безопасность и конфиденциальность, вы попали по адресу.""",
                             reply_markup=ikb.user_panel)
        await set_user(message.from_user.id, message.from_user.full_name, current_date)
        await message.answer(f"Вы успешно авторизовались как администратор!",
                             reply_markup=rkb.admin_menu)


@user.callback_query(F.data == "buy")
async def buy(callback: CallbackQuery):
    await callback.message.edit_text("<b>Выберите страну:</b>",
                                     reply_markup=await bkb.user_vpn_categories())


@user.callback_query(F.data.startswith("category_"))
async def user_choose_category(callback: CallbackQuery):
    vpn_category_id = int(callback.data.split("_")[1])

    await callback.message.edit_text("<b>Тариф:</b>",
                                     reply_markup=await bkb.user_countries(vpn_category_id))


@user.callback_query(F.data.startswith("country_"))
async def user_choose_country(callback: CallbackQuery, bot: Bot):
    vpn_id = int(callback.data.split("_")[1])

    await create_payment_one(callback, bot, vpn_id)


