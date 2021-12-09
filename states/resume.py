from aiogram.dispatcher.filters.state import StatesGroup, State


class ResumeState(StatesGroup):
    P_LANGUAGES = State()
    DB = State()
    EX_YEAR = State()
    LANGUAGES = State()
    EDUCATION_D = State()
    BIO = State()
    # here, we set which questions are interested us
    UPDATE = State()  # update or create ?
