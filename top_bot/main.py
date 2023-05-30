import asyncio
from aiogram import Bot
import top_bot.core.io as io_layer
from top_bot.core.settings import settings

async def on_startup(bot: Bot):
    await bot.send_message(settings.bots.admin_id, "Бот включен")

async def on_shutdown(bot: Bot):
    await bot.send_message(settings.bots.admin_id, "Бот отключен")

async def load_bot():
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = io_layer.start.dispatch()
    groups = io_layer.group.dispatch()
    subjects = io_layer.subject.dispatch()
    media = io_layer.media.dispatch()

    io_layer.dispatch_errors([media, subjects, groups, dp])

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