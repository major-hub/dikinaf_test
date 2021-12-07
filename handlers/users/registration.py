from aiogram import types
from aiogram.dispatcher.filters import Text

from keyboards.default.registration import btn_registration
from loader import dp


@dp.message_handler(Text(equals=btn_registration[0][0]))
async def start_registration(message: types.Message):
    await message.answer("Start Registration")

# all_state then own states
