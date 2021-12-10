import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data import config
from utils.db_api.postgresql import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# storage = RedisStorage2()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
loop = asyncio.get_event_loop()
loop.run_until_complete(db.create())  # is need to create pool
loop.run_until_complete(db.create_table_profile())  # is need to create pool
loop.run_until_complete(db.create_table_resume())  # is need to create pool
