import asyncio
from typing import Any

from aiogram import Bot
from aiogram.types import Message

from db import User
from parser import OkParser


async def check_user(tg_id: int, login=None, password=None):
    r = await User.get_user(User(tg_id=tg_id, login=login, password=password))
    print(f"result{r}")
    return r


async def create_user(user_data: dict[str, Any]):
    tg_id = user_data.get('tg_id')
    if await check_user(tg_id) is not None:
        login = user_data.get('login')
        password = user_data.get('password')
        await User.create(User(login=login, password=password, tg_id=tg_id))
    else:
        pass


async def check_last_post():
    return await OkParser.check_post()

