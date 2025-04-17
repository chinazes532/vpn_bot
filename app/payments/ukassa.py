import asyncio
import uuid
from datetime import datetime

from aiogram import Bot
from dateutil.relativedelta import relativedelta
from yookassa import Payment, Configuration
from aiogram.types import CallbackQuery

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb
from app.outline_vpn.outline_vpn import OutlineVPN

from config import ADMINS, ACCOUNT_ID, SECRET_KEY

from app.database.requests.vpns.select import get_vpn_by_id

Configuration.account_id = ACCOUNT_ID
Configuration.secret_key = SECRET_KEY


async def create_payment_one(callback: CallbackQuery, bot: Bot, vpn_id):
    vpn = await get_vpn_by_id(vpn_id)
    payment = Payment.create({
        "amount": {
            "value": f"{vpn.price}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/Natali_clubBot"
        },
        "capture": True,
        "description": f"{vpn.name}",
    }, uuid.uuid4())

    await callback.message.edit_text(f"<b>Вы выбрали тариф {vpn.name}\n"
                                     f"Для оплаты на сумму {vpn.price} ₽ нажмите на кнопку \"Оплатить\"</b>",
                                     reply_markup=await bkb.ukassa_pay(payment.confirmation.confirmation_url))

    asyncio.create_task(check_payment_status_one(payment.id, callback, bot, vpn_id))


async def check_payment_status_one(payment_id: str, callback: CallbackQuery, bot: Bot, vpn_id):
    while True:
        payment = Payment.find_one(payment_id)
        if payment.status == "succeeded":
            await finalize_payment_one(callback, bot, vpn_id)
            break

        await asyncio.sleep(3)


async def finalize_payment_one(callback: CallbackQuery, bot: Bot, vpn_id):
    vpn = await get_vpn_by_id(vpn_id)
    tg_id = callback.from_user.id

    client = OutlineVPN(vpn.server_ip, vpn.server_hash)

    key = await client.create_key(
        name=f"{callback.from_user.full_name}",
        data_limit=1024 * 1024 * 20,
        method="aes-192-gcm"
    )

    await bot.send_message(chat_id=tg_id,
                           text=f"Ваш ключ:\n\n<code>{key.access_url}</code>",)
    for admin in ADMINS:
        await bot.send_message(chat_id=admin,
                               text=f'<b>❗️Новая оплата❗️\n'
                                    f'Пользователь <a href="tg://user?id={tg_id}">{callback.from_user.full_name}</a>\n'
                                    f'Название тарифа: {vpn.name}\n'
                                    f'Cтоимость: {vpn.price}\n'
                                    f'Способ оплаты: ЮКАССА</b>',
                               parse_mode='HTML')






