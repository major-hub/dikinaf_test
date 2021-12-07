from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class ModeratorFilter(BoundFilter):
    key = 'is_moderator'

    def __init__(self, is_moderator):
        self.is_moderator = is_moderator

    async def check(self, message: Message) -> bool:
        user_id = message.from_user.id
        return await db.is_moderator(user_id)
