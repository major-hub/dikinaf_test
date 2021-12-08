from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.registration import btn_registration, btn_menu_user_without_resume, btn_menu_user_with_resume
from loader import dp, db


# @dp.message_handler(CommandStart(), is_admin=True)
# async def bot_start_admin(message: types.Message):
#     await message.answer(f"You are admin")


@dp.message_handler(CommandStart(), is_moderator=True)
async def bot_start_moderator(message: types.Message):
    await message.answer("You are moderator")


@dp.message_handler(CommandStart(), is_registrated=True)
async def bot_start_registrated(message: types.Message):
    have_resume = await db.have_my_resume(message.from_user.id)
    if have_resume:
        markup = types.ReplyKeyboardMarkup(btn_menu_user_with_resume, True)
    else:
        markup = types.ReplyKeyboardMarkup(btn_menu_user_without_resume, True)
    await message.answer("Choose one of the below", reply_markup=markup)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(btn_registration, True)
    await message.answer("Please, register", reply_markup=markup)
