from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")

PG_NAME = env.str("PG_NAME")
PG_USER = env.str("PG_USER")
PG_PASSWORD = env.str("PG_PASSWORD")
