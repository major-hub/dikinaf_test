from aiogram import types
from loader import db


async def btn_moderators():
    moderators = await db.get_moderators()
    keyboard = [
        [types.InlineKeyboardButton(m[1], callback_data=f"m:{m[0]}")]
        for m in moderators
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def btn_ball(telegram_id):
    return [[
        types.InlineKeyboardButton("1️⃣", callback_data=f"b:1:{telegram_id}"),
        types.InlineKeyboardButton("2️⃣", callback_data=f"b:2:{telegram_id}"),
        types.InlineKeyboardButton("3️⃣", callback_data=f"b:3:{telegram_id}"),
        types.InlineKeyboardButton("4️⃣", callback_data=f"b:4:{telegram_id}"),
        types.InlineKeyboardButton("5️⃣", callback_data=f"b:5:{telegram_id}")
    ]]
