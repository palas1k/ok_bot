import asyncio
from typing import Any

from aiogram import Bot
from aiogram.types import Message

from db import User, UserCounter
from parser import OkParser, Auth


async def check_user(tg_id: int):
    r = await User.get_user(tg_id=tg_id)
    return r


async def create_user(user_data: dict[str, Any]):
    tg_id = user_data.get('tg_id')
    if await check_user(tg_id) is None:
        login = user_data.get('login')
        password = user_data.get('password')
        await User.create(User(login=login, password=password, tg_id=tg_id))
    else:
        pass


async def check_last_post(message: Message) -> str:
    runner = OkParser()
    res = await runner.check_post()
    await message.answer(res)


async def perform_login(login: str, password: str) -> bool:
    r_ = Auth()
    res = await r_.perform_login(login, password)
    if str(res.real_url) == "https://ok.ru/?just-logged-in=true":
        return True
    else:
        return False


async def check_user_in_counter(user_id: int):
    r = await UserCounter.get_user(user_id=user_id)
    return r


async def counter_plus(user_id: int):
    return await UserCounter.plus_count(user_id)


async def get_or_create_user_in_counter(user_id: int):
    if await check_user_in_counter(user_id) is None:
        await UserCounter.create(user_id=user_id)
    else:
        await counter_plus(user_id)



