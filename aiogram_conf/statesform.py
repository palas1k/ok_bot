from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_LOGIN = State()
    GET_PASSWORD = State()


class StepsBio(StatesGroup):
    GET_ID = State()
