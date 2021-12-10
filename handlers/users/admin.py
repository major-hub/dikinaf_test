from aiogram import types
from aiogram.dispatcher.filters import Text, Command

from keyboards.default.admin import btn_admin_menu
from loader import dp, db


@dp.message_handler(Text(equals=btn_admin_menu[0][0]), is_admin=True)
async def handle_admin_moderators(message: types.Message):
    text = "To add moderator:\n /set `moderator's telegram_id`\n\n" \
           "To remove moderator: \n /unset `moderator's telegram_id`"
    await message.answer(text, parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(Text(equals=btn_admin_menu[1][0]), is_admin=True)
async def handle_admin_statistics(message: types.Message):
    stats = await db.get_statistics()
    if stats:
        text = "\n".join(
            [f"`Moderator: {stat[1]}\tEstimated: {stat[0]}`" for stat in stats]
        )
    else:
        text = "Moderators haven't estimated yet"
    await message.answer(text, parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(Command('set'), is_admin=True)
async def handle_admin_set(message: types.Message):
    telegram_id = int(message.text.split('/set')[-1].strip())
    is_registrated = await db.is_registrated(telegram_id)
    if is_registrated:
        await db.set_moderator(telegram_id)
        text = "`User -> Moderator`"
        await message.answer(text, parse_mode=types.ParseMode.MARKDOWN)
    else:
        text = "User not found!"
        await message.answer(text)


@dp.message_handler(Command('unset'), is_admin=True)
async def handle_admin_set(message: types.Message):
    telegram_id = int(message.text.split('/unset')[-1].strip())
    is_registrated = await db.is_registrated(telegram_id)
    if is_registrated:
        await db.unset_moderator(telegram_id)
        text = "`Moderator -> User`"
        await message.answer(text, parse_mode=types.ParseMode.MARKDOWN)
    else:
        text = "User not found!"
        await message.answer(text)
