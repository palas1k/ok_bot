import asyncio

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram_conf.basic import create_user, perform_login, get_or_create_user_in_counter
from aiogram_conf.statesform import StepsForm, StepsBio
from parser import Auth, OkParser


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
    r_ = await perform_login(login, password)
    if r_:
        await message.answer('Logged In')
    else:
        await message.answer("Something wrong, Non logged")
    await state.clear()


async def get_user_id(message: Message, state: FSMContext):
    await message.answer(f"Введите id кого будем искать")
    await state.set_state(StepsBio.GET_ID)


async def get_info(message: Message, state: FSMContext):
    OP = OkParser()
    a = Auth()
    try:
        id = int(message.text)
        if a.session:
            r = await OP.get_bio(id)
            await get_or_create_user_in_counter(id)
            await message.answer(r)
        else:
            await message.answer("Сначала залогинься /login")
    except Exception as ex:
        print(ex)
        await message.answer("Что то пошло не так")
    finally:
        await state.clear()