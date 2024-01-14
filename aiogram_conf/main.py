import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_conf import form, basic
from aiogram_conf.basic import check_last_post
from aiogram_conf.commands import set_commands
from aiogram_conf.form import get_user_id, get_info
from aiogram_conf.statesform import StepsForm, StepsBio
from parser import OkParser
from settings import stngs

bot = Bot(stngs.bots.bot_token)
dp = Dispatcher()


async def with_bot_start(bot: Bot):
    await set_commands(bot)
    await bot.send_message(stngs.bots.admin_id, f"Bot start {datetime.now()}")


async def start():
    logging.basicConfig(level=logging.INFO)
    dp.startup.register(with_bot_start)
    dp.message.register(form.get_form, Command(commands='login'))
    dp.message.register(form.get_login, StepsForm.GET_LOGIN)
    dp.message.register(form.get_password, StepsForm.GET_PASSWORD)
    dp.message.register(check_last_post, Command(commands='post'))
    dp.message.register(get_user_id, Command(commands='bio'))
    dp.message.register(get_info, StepsBio.GET_ID)

    try:
        await dp.start_polling(bot)
    except Exception as ex:
        print(ex)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())
