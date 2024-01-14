from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_LOGIN = State()
    GET_PASSWORD = State()