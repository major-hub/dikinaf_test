from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(state=None)
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer(f"Эхо без состояния."
                         f"Сообщение:\n"
                         f"{message.text}")


@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    await message.answer(f"Эхо в состоянии <code>{await state.get_state()}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")
    await state.finish()
