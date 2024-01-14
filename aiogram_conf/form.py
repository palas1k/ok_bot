from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram_conf.basic import create_user
from aiogram_conf.statesform import StepsForm


async def get_form(message: Message, state: FSMContext):
    await message.answer(f"{message.from_user.first_name}, заходим в ok.ru. Введите свой логин")
    await state.set_state(StepsForm.GET_LOGIN)


async def get_login(message: Message, state: FSMContext):
    await message.answer(f"Отлично теперь пароль")
    await state.update_data(login=message.text)
    await state.update_data(tg_id=message.from_user.id)
    await state.set_state(StepsForm.GET_PASSWORD)


async def get_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    context_data = await state.get_data()
    login = context_data.get('login')
    password = context_data.get('password')
    user_data = f"Твои данные\r\n" \
                f"Логин {login}\r\n" \
                f"Пароль {password}\r\n" \
                f"TG Id {message.from_user.id}"
    await create_user(context_data)
    await message.answer(user_data)
    await state.clear()

