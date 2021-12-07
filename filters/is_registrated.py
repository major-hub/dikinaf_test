from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class RegistratedFilter(BoundFilter):
    key = 'is_registrated'

    def __init__(self, is_registrated):
        self.is_registrated = is_registrated

    async def check(self, message: Message) -> bool:
        user_id = message.from_user.id
        return await db.is_registrated(user_id)
