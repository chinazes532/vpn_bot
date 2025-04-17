from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb


back = Router()


@back.callback_query(F.data == "user_back")
async def user_back(callback: CallbackQuery):
    await callback.message.edit_text(f"""🌐 <b>Добро пожаловать!</b> 🌐

Мы рады видеть вас здесь! 
Если вы ищете надежный способ обеспечить свою онлайн-безопасность и конфиденциальность, вы попали по адресу.""",
                             reply_markup=ikb.user_panel)