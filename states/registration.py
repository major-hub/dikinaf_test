from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationState(StatesGroup):
    FULL_NAME = State()
    BIRTHDAY = State()
    PHONE_NUMBER = State()
