import datetime
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.default.registration import btn_registration, btn_phone_number, btn_menu_user_without_resume
from loader import dp, db
from states.registration import RegistrationState


@dp.message_handler(Text(equals=btn_registration[0][0]))
async def start_registration(message: types.Message):
    await RegistrationState.FULL_NAME.set()
    markup = types.ReplyKeyboardRemove()
    await message.answer("Enter your full FIO", reply_markup=markup)


@dp.message_handler(state=RegistrationState.all_states, commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state=RegistrationState.all_states)
async def registration_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    text = "Cancelled."
    markup = types.ReplyKeyboardRemove()
    await message.reply(text, reply_markup=markup)


@dp.message_handler(Text(startswith=['/', '!']), state=RegistrationState.FULL_NAME, content_types=types.ContentType.ANY)
async def handle_full_name_invalid(message: types.Message, state: FSMContext):
    state = await state.get_state()
    logging.error(state)
    await message.answer("Please enter the valid FIO")


@dp.message_handler(state=RegistrationState.FULL_NAME, content_types=types.ContentType.TEXT)
async def handle_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['telegram_id'] = message.from_user.id
        data['full_name'] = message.text

    await RegistrationState.next()
    text = "Enter your birthday like the format below\n\n`dd.mm.yyyy`"
    await message.answer(text, parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(state=RegistrationState.BIRTHDAY, content_types=types.ContentType.TEXT)
async def handle_birthday(message: types.Message, state: FSMContext):
    try:
        date = datetime.datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        await message.answer("Please Enter the valid Birthday\n\n`dd.mm.yyyy`", parse_mode=types.ParseMode.MARKDOWN)
        return
    now = datetime.datetime.now().year
    if date.year < now - 100 or date.year > now - 7:
        await message.answer("Please Enter the valid Birthday\n\n`dd.mm.yyyy`", parse_mode=types.ParseMode.MARKDOWN)
        return

    async with state.proxy() as data:
        data['birthday'] = message.text
    text = "Click the button below or send your Phone Number like the format below\n\n`90 123 45 67`"
    markup = types.ReplyKeyboardMarkup(btn_phone_number, True)
    await RegistrationState.next()
    await message.answer(text, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(state=RegistrationState.PHONE_NUMBER, content_types=types.ContentType.CONTACT)
async def handle_phone_number_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
        try:
            await db.add_profile(**data)
        except Exception as e:
            logging.error(e)
            markup = types.ReplyKeyboardMarkup(btn_registration, True)
            await state.finish()
            await message.answer("Something went wrong!\nTry again", reply_markup=markup)
            return

    await state.finish()
    markup = types.ReplyKeyboardMarkup(btn_menu_user_without_resume, True)
    await message.answer("Registration completed successfully!", reply_markup=markup)


@dp.message_handler(state=RegistrationState.PHONE_NUMBER, content_types=types.ContentType.TEXT)
async def handle_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text.replace(' ', '')
    if not phone_number.isdigit() or len(phone_number) != 9:
        text = "Please, enter the valid Phone Number\n\n`90 123 45 67`"
        await message.answer(text, parse_mode=types.ParseMode.MARKDOWN)
        return

    async with state.proxy() as data:
        data['phone_number'] = phone_number
        try:
            await db.add_profile(**data)
        except Exception as e:
            logging.error(e)
            markup = types.ReplyKeyboardMarkup(btn_registration, True)
            await state.finish()
            await message.answer("Something went wrong!\nTry again", reply_markup=markup)
            return

    await state.finish()
    markup = types.ReplyKeyboardMarkup(btn_menu_user_without_resume, True)
    await message.answer("Registration completed successfully!", reply_markup=markup)
