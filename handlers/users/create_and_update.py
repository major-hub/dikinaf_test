import asyncio
import os
from pathlib import Path

from aiogram import types
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, db

from keyboards.default.resume import (
    btn_menu_user_with_resume as b_with,
    btn_menu_user_without_resume as b_without,
    btn_change_or_cancel as b_c_or_u, btn_menu_user_with_resume
)
from states.resume import ResumeState
from utils.create_pdf import pdf_create


@dp.message_handler(Text(equals=[b_with[0][0], b_without[0][0]]), is_registrated=True)
async def handle_create_or_update(message: types.Message):
    await ResumeState.P_LANGUAGES.set()
    text = "Which programming languages do you know?\n\n`e.x: Python, C++, GO`"
    markup = types.ReplyKeyboardRemove()
    await message.answer(text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=ResumeState.all_states, commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state=ResumeState.all_states)
async def create_or_update_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    text = "Cancelled."
    markup = types.ReplyKeyboardRemove()
    await message.reply(text, reply_markup=markup)


@dp.message_handler(state=ResumeState.P_LANGUAGES, content_types=types.ContentType.TEXT)
async def handle_p_languages(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['p_languages'] = message.text
    await ResumeState.next()
    text = "Which databases do you usually use?\n\n`e.x: PostgreSql, MySql, Redis`"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=ResumeState.DB, content_types=types.ContentType.TEXT)
async def handle_db(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['db'] = message.text
    await ResumeState.next()
    text = "Work experience (in years)?\n\n`e.x: 1year, 2year or 5+year`"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=ResumeState.EX_YEAR, content_types=types.ContentType.TEXT)
async def handle_ex_year(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ex_year'] = message.text
    await ResumeState.next()
    text = "Which languages do you know?\n\n`e.x: English little, Uzbek native, Russian enough for work`"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=ResumeState.LANGUAGES, content_types=types.ContentType.TEXT)
async def handle_languages(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['languages'] = message.text
    await ResumeState.next()
    text = "Which education degree?\n\n`e.x: Bachelor or Master`"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=ResumeState.EDUCATION_D, content_types=types.ContentType.TEXT)
async def handle_education_d(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['education_d'] = message.text
    await ResumeState.next()
    text = "Write a little about yourself"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=ResumeState.BIO, content_types=types.ContentType.TEXT)
async def handle_bio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        full_name = await db.get_full_name(message.from_user.id)
        phone_number = await db.get_phone_number(message.from_user.id)
        data['full_name'] = full_name
        data['phone_number'] = phone_number
        data['bio'] = message.text
        data['telegram_id'] = message.from_user.id
        pdf_create(data)
        await asyncio.sleep(1.0)

    is_have = await db.have_my_resume(message.from_user.id)
    root_dir = Path(__file__).parent.parent.parent
    if is_have:
        await ResumeState.next()
        old_path = root_dir / f"media/resumes/{str(message.from_user.id)}.pdf"
        new_path = root_dir / f"media/temp/{str(message.from_user.id)}_new.pdf"
        await message.answer_document(types.InputFile(old_path, filename="Old Resume.pdf"))
        await message.answer_document(types.InputFile(new_path, filename="New Resume.pdf"))
        text = "You really want to change ?"
        markup = types.ReplyKeyboardMarkup(b_c_or_u, True)
        await message.answer(text, reply_markup=markup)
    else:
        old_path = root_dir / f"media/temp/{str(message.from_user.id)}_new.pdf"
        new_path = root_dir / f"media/resumes/{str(message.from_user.id)}.pdf"
        os.replace(old_path, new_path)
        await db.set_resume_path(message.from_user.id)
        await state.finish()
        await message.answer_document(types.InputFile(str(new_path)))
        text = "Your Resume created successfully!"
        markup = types.ReplyKeyboardMarkup(btn_menu_user_with_resume, True)
        await message.answer(text, reply_markup=markup)


@dp.message_handler(Text(equals=b_c_or_u[0]), state=ResumeState.UPDATE, content_types=types.ContentType.TEXT)
async def handle_update(message: types.Message, state: FSMContext):
    root_dir = Path(__file__).parent.parent.parent

    if message.text == b_c_or_u[0][0]:
        old_path = root_dir / f"media/temp/{str(message.from_user.id)}_new.pdf"
        new_path = root_dir / f"media/resumes/{str(message.from_user.id)}.pdf"
        os.replace(old_path, new_path)
        await db.set_resume_path(message.from_user.id)
        await db.set_resume_ball_null(message.from_user.id)
        await state.finish()
        text = "Your Resume changed successfully !"
        markup = types.ReplyKeyboardMarkup(btn_menu_user_with_resume, True)
        await message.answer(text, reply_markup=markup)
    else:
        path = root_dir / f"media/temp/{str(message.from_user.id)}_new.pdf"
        os.remove(path)
        await state.finish()
        text = "Your Resume not modified !"
        markup = types.ReplyKeyboardMarkup(btn_menu_user_with_resume, True)
        await message.answer(text, reply_markup=markup)
