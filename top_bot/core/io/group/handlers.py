from aiogram import Router
from aiogram.handlers import MessageHandler, CallbackQueryHandler

def dispatch() -> Router:
    groups = Router(name="groups")
    return groups

class ListGroups(CallbackQueryHandler):
    async def handle(self):
        return await super().handle()

class RetrieveGroup(CallbackQueryHandler):
    async def handle(self):
        return await super().handle()
    
class CreateGroup(CallbackQueryHandler):
    async def handle(self):
        return await super().handle()