from aiogram import Router
from aiogram.handlers import MessageHandler, CallbackQueryHandler


def dispatch():
    media = Router(name="media")
    return media

class ListMedia(CallbackQueryHandler):
    async def handle(self):
        return await super().handle()
    
class AddMedia(CallbackQueryHandler):
    async def handle(self):
        return await super().handle()