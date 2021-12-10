from pathlib import Path

from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import db, dp
from keyboards.default.resume import (
    btn_menu_user_with_resume as b_with,
    btn_menu_user_without_resume as b_without
)


@dp.message_handler(Text(equals=[b_with[1][0], b_without[1][0]]), is_moderator=True)
async def handle_get_my_resume_m(message: types.Message):
    pass


@dp.message_handler(Text(equals=[b_with[1][0], b_without[1][0]]), is_registrated=True)
async def handle_get_my_resume(message: types.Message):
    is_have = await db.have_my_resume(message.from_user.id)
    if is_have:
        root_dir = Path(__file__).parent.parent.parent
        path = root_dir / f"media/resumes/{str(message.from_user.id)}.pdf"
        await message.answer_document(types.InputFile(path, filename="Your resume.pdf"))
    else:
        text = "You haven't created resume yet"
        await message.answer(text)
