import asyncio
import os
from aiogram import Bot
import top_bot.core.io as io_layer
from top_bot.core.settings import settings
from top_bot.utils.commands import set_commands

async def on_startup(bot: Bot):
    await set_commands(bot)

    try:
        os.mkdir(settings.bots.root_dir)
        os.mkdir(settings.bots.media_store)
    except FileExistsError:
        pass

    try:
        open(settings.bots.users_list, "x")
    except FileExistsError:
        pass

    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')

async def on_shutdown(bot: Bot):
    await bot.send_message(settings.bots.admin_id, "Бот отключен")

async def load_bot():
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = io_layer.start.dispatch()
    groups = io_layer.group.dispatch()
    subjects = io_layer.subject.dispatch()
    media = io_layer.media.dispatch()

    io_layer.base_dispatch([media, subjects, groups, dp])

    subjects.include_router(media)
    groups.include_router(subjects)
    dp.include_router(groups)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

def load():
    asyncio.run(load_bot())