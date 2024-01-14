from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='login',
            description='Login in ok.ru'
        ),
        BotCommand(
            command='write',
            description='send message in ok'
        ),
        BotCommand(
            command='post',
            description='my post'
        )
    ]

    await bot.set_my_commands(commands)
