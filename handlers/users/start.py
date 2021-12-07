from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.registration import btn_registration
from loader import dp


# @dp.message_handler(CommandStart(), is_admin=True)
# async def bot_start(message: types.Message):
#     await message.answer(f"Siz adminsiz")


@dp.message_handler(CommandStart(), is_moderator=True)
async def bot_start(message: types.Message):
    await message.answer("Siz moderatorsiz")


@dp.message_handler(CommandStart(), is_registrated=True)
async def bot_start(message: types.Message):
    await message.answer("Siz royhatdan otgansiz")


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(btn_registration, True)
    await message.answer("Iltimos, royhatdan oting", reply_markup=markup)
