import asyncio
import os.path
import asyncpg

from pathlib import Path
from typing import Union
from datetime import datetime, timedelta
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        pool = await asyncpg.create_pool(
            database=config.PG_NAME,
            user=config.PG_USER,
            password=config.PG_PASSWORD,
            host='localhost'
        )
        self.pool = pool

    @property
    def now(self):
        return datetime.utcnow() + timedelta(hours=5)

    @property
    def root_dir(self):
        return Path(__file__).parent.parent.parent

    @property
    def base_path(self):
        return f"media/resumes/"

    async def create_table_profile(self, force=False):
        if force:
            sql = "DROP TABLE IF EXISTS profile CASCADE;"
            await self.pool.execute(sql)

        sql = """
            CREATE TABLE IF NOT EXISTS profile (
                telegram_id INTEGER PRIMARY KEY UNIQUE,
                full_name VARCHAR NOT NULL ,
                birthday VARCHAR NOT NULL ,
                phone_number VARCHAR NOT NULL ,
                is_moderator BOOLEAN DEFAULT FALSE NOT NULL ,
                resume_path VARCHAR,
                resume_ball INTEGER,
                registrated_at TIMESTAMP NOT NULL 
            );
        """
        await self.pool.execute(sql)

    async def create_table_resume(self, force=False):
        if force:
            sql = "DROP TABLE IF EXISTS resume CASCADE;"
            await self.pool.execute(sql)

        sql = """
            CREATE TABLE IF NOT EXISTS resume (
                id SERIAL PRIMARY KEY ,
                user_id INTEGER NOT NULL ,
                moderator_id INTEGER,
                ball INTEGER,
                estimated_at TIMESTAMP
            );
        """
        await self.pool.execute(sql)

    async def create_resume(self, user_id: int):
        sql = "INSERT INTO resume (user_id) VALUES ($1);"
        await self.pool.execute(sql, user_id)

    async def have_in_process(self, user_id: int):
        sql = "SELECT TRUE FROM resume WHERE user_id=$1 and ball IS NULL;"
        in_process = await self.pool.fetchrow(sql, user_id)
        return True if in_process is not None else False

    async def estimate_resume(self, moderator_id: int, user_id: int, ball: int):
        sql = """
            UPDATE resume SET moderator_id=$1, ball=$2, estimated_at=$3
            WHERE user_id=$4 and ball IS NULL;    
        """
        await self.pool.execute(sql, moderator_id, ball, self.now, user_id)

    async def add_profile(self, telegram_id: int, full_name, birthday, phone_number):
        sql = """
            INSERT INTO profile (telegram_id, full_name, birthday, phone_number, registrated_at) 
            VALUES ($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING;
        """
        await self.pool.execute(sql, telegram_id, full_name, birthday, phone_number, self.now)

    async def get_full_name(self, telegram_id: int):
        sql = "SELECT full_name FROM profile WHERE telegram_id=$1;"
        full_name = await self.pool.fetchrow(sql, telegram_id)
        return full_name[0]

    async def get_phone_number(self, telegram_id: int):
        sql = "SELECT phone_number FROM profile WHERE telegram_id=$1;"
        phone_number = await self.pool.fetchrow(sql, telegram_id)
        return phone_number[0]

    async def set_resume_path(self, telegram_id):
        path = self.base_path + f"{str(telegram_id)}.pdf"
        sql = "UPDATE profile SET resume_path=$2 WHERE telegram_id=$1;"
        await self.pool.execute(sql, telegram_id, path)

    async def set_resume_ball(self, telegram_id: int, ball: int):
        sql = "UPDATE profile SET resume_ball=$2 WHERE telegram_id=$1;"
        await self.pool.execute(sql, telegram_id, ball)

    async def set_resume_ball_null(self, telegram_id: int):
        sql = "UPDATE profile SET resume_ball=NULL WHERE telegram_id=$1;"
        await self.pool.execute(sql, telegram_id)

    async def get_resume_ball(self, telegram_id: int):
        sql = "SELECT resume_ball FROM profile WHERE telegram_id=$1;"
        resume_ball = await self.pool.fetchrow(sql, telegram_id)
        return resume_ball[0]

    async def have_my_resume(self, telegram_id: int):
        sql = "SELECT TRUE FROM profile WHERE telegram_id=$1 AND resume_path IS NOT NULL"
        resume = await self.pool.fetchrow(sql, telegram_id)
        is_have = True if resume is not None else False
        if is_have:
            path = await self.get_my_resume_path(telegram_id)
            return os.path.isfile(self.root_dir / path)
        return False

    async def get_my_resume_path(self, telegram_id: int):
        sql = "SELECT resume_path FROM profile WHERE telegram_id=$1;"
        resume_path = await self.pool.fetchrow(sql, telegram_id)
        return resume_path[0]

    async def set_moderator(self, telegram_id: int):
        sql = "UPDATE profile SET is_moderator=TRUE WHERE telegram_id=$1;"
        await self.pool.execute(sql, telegram_id)

    async def unset_moderator(self, telegram_id: int):
        sql = "UPDATE profile SET is_moderator=FALSE WHERE telegram_id=$1;"
        await self.pool.execute(sql, telegram_id)

    async def get_moderators(self):
        sql = "SELECT telegram_id, full_name FROM profile WHERE is_moderator=TRUE;"
        moderators = await self.pool.fetch(sql)
        return moderators

    async def is_moderator(self, telegram_id: int):
        sql = "SELECT TRUE FROM profile WHERE telegram_id=$1 AND is_moderator=TRUE;"
        moderator = await self.pool.fetchrow(sql, telegram_id)
        return True if moderator is not None else False

    async def is_registrated(self, telegram_id: int):
        sql = "SELECT TRUE FROM profile WHERE telegram_id=$1;"
        user = await self.pool.fetchrow(sql, telegram_id)
        return True if user is not None else False

    async def get_statistics(self):
        sql = "SELECT COUNT(id), moderator_id FROM resume WHERE ball IS NOT NULL GROUP BY (moderator_id);"
        stats = await self.pool.fetch(sql)
        return stats


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    dd = Database()
    loop.run_until_complete(dd.create())
    loop.run_until_complete(dd.create_table_profile())
    loop.run_until_complete(dd.create_table_resume())
    loop.run_until_complete(dd.add_profile(
        telegram_id=621383782,
        full_name="Solijonov Otabek3",
        birthday="30.09.1999",
        phone_number="998911144735"
    ))
    # loop.run_until_complete(dd.set_resume_path(621383789))  # passed
    # print(loop.run_until_complete(dd.have_my_resume(621383789)))  # passed
    # print(loop.run_until_complete(dd.get_full_name(621383789)))  # passed
    # print(loop.run_until_complete(dd.get_my_resume_path(621383789)))  # passed
    # print(loop.run_until_complete(dd.set_moderator(621383782)))  # passed
    # print(loop.run_until_complete(dd.get_moderator_ids()))  # passed
    # print(loop.run_until_complete(dd.get_statistics()))  # passed
