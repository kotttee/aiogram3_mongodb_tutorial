from aiogram.fsm.state import StatesGroup, State


class Settings(StatesGroup):
    accept = State()
    age = State()
