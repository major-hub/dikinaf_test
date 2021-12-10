from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp

from keyboards.default.resume import (
    btn_menu_user_with_resume as b_with,
    btn_menu_user_without_resume as b_without
)


@dp.message_handler(Text(equals=[b_with[1][1], b_without[1][1]]), is_registrated=True)
async def handle_settings(message: types.Message):
    await message.answer("Not completed!")
