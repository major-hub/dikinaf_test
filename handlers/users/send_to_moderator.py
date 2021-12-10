from pathlib import Path

from aiogram import types
from aiogram.dispatcher.filters import Text

from keyboards.inline.moderators import btn_moderators, btn_ball
from loader import db, dp, bot
from keyboards.default.resume import (
    btn_menu_user_with_resume as b_with,
    btn_menu_user_without_resume as b_without
)


@dp.message_handler(Text(equals=[b_with[0][1], b_without[0][1]]), is_moderator=True)
async def handle_send_to_moderator_m(message: types.Message):
    await message.answer("You are Moderator")


@dp.message_handler(Text(equals=[b_with[0][1], b_without[0][1]]), is_registrated=True)
async def handle_send_to_moderator(message: types.Message):
    is_have = await db.have_my_resume(message.from_user.id)
    if is_have:
        resume_ball = await db.get_resume_ball(message.from_user.id)
        if resume_ball is not None:
            text = f"Moderators estimated your resume with {resume_ball} ball"
            await message.answer(text)
        else:
            in_process = await db.have_in_process(message.from_user.id)
            if in_process:
                text = "Your resume is in process!\nPlease, wait..."
                await message.answer(text)
            else:
                text = "Choose one moderator"
                markup = await btn_moderators()
                await message.answer(text, reply_markup=markup)
    else:
        text = "You haven't created resume yet"
        await message.answer(text)


@dp.callback_query_handler(Text(startswith='m:'))
async def handle_choose_moderator(query: types.CallbackQuery):
    await query.answer("Wait for the moderator's answer")
    _, moderator_id = query.data.split(':')
    root_dir = Path(__file__).parent.parent.parent
    path = root_dir / f"media/resumes/{str(query.from_user.id)}.pdf"
    await db.create_resume(query.from_user.id)

    text = "You need to check and estimate this resume"
    keyboard = btn_ball(query.from_user.id)
    markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    await bot.send_document(moderator_id, types.InputFile(path), caption=text, reply_markup=markup)
    await bot.delete_message(query.from_user.id, query.message.message_id)


@dp.callback_query_handler(Text(startswith='b:'))
async def handle_ball(query: types.CallbackQuery):
    await query.answer("You set the ball")
    _, ball, user_id = query.data.split(':')
    await db.set_resume_ball(int(user_id), int(ball))
    await db.estimate_resume(query.from_user.id, int(user_id), int(ball))

    text = f"Moderator estimate your resume with {ball} ball"
    await bot.send_message(user_id, text)
    await bot.delete_message(query.from_user.id, query.message.message_id)
