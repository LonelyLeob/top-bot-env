from aiogram.handlers import MessageHandler, CallbackQueryHandler
from aiogram import Router
from top_bot.core.io import base


def dispatch() -> Router:
    subjects = Router(name="subjects")
    return subjects

class Start(MessageHandler):
    async def handle(self):
        return await super().handle()
    
class Start(CallbackQueryHandler):
    async def handle(self):
        return await super().handle()
    
class Start(MessageHandler):
    async def handle(self):
        return await super().handle()
    
class Start(MessageHandler):
    async def handle(self):
        return await super().handle()
    