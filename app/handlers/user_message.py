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

from app.outline.api import create_access_key, get_access_key_url

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
                             reply_markup=await bkb.user_vpn_categories())
        await set_user(message.from_user.id, message.from_user.full_name, current_date)
    else:
        await message.answer(f"""🌐 <b>Добро пожаловать!</b> 🌐

Мы рады видеть вас здесь! 
Если вы ищете надежный способ обеспечить свою онлайн-безопасность и конфиденциальность, вы попали по адресу.""",
                             reply_markup=await bkb.user_vpn_categories())
        await set_user(message.from_user.id, message.from_user.full_name, current_date)
        await message.answer(f"Вы успешно авторизовались как администратор!",
                             reply_markup=rkb.admin_menu)


@user.callback_query(F.data.startswith("category_"))
async def user_choose_category(callback: CallbackQuery):
    await callback.answer("Выбор региона. . .")

    vpn_category_id = int(callback.data.split("_")[1])

    await callback.message.edit_text("<b>Выберите регион:</b>",
                                     reply_markup=await bkb.user_countries(vpn_category_id))


@user.callback_query(F.data.startswith("country_"))
async def user_choose_country(callback: CallbackQuery):
    vpn_id = int(callback.data.split("_")[1])
    vpn = await get_vpn_by_id(vpn_id)

    if vpn.max_conn <= vpn.current_conn:
        await callback.answer("Мест на данный VPN больше нет!",
                              show_alert=True)
        return

    await callback.message.edit_text(f"<b>{vpn.name}</b>\n"
                                     f"Цена: {vpn.price} RUB в месяц\n")

    vpn_data = await create_access_key(vpn.server_ip, vpn.server_hash)

    if 'key' in vpn_data:
        print(f"Создан ключ: {vpn_data['key']}")
    else:
        print(f"Ошибка при создании ключа: {vpn_data}")


@user.message(Command("get"))
async def get(message: Message):
    key = await get_access_key_url("1")

    print(key)