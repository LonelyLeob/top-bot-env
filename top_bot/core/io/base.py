from aiogram.handlers import ErrorHandler
from aiogram.types import ErrorEvent
from aiogram import Router
from top_bot.core.settings import settings
from aiogram.types.user import User

def dispatch_errors(routers: list[Router]):
    for router in routers:
        router.errors.register(ProduceError)

class ProduceError(ErrorHandler):
    event: ErrorEvent
    async def handle(self):
        user: User = self.data["event_from_user"]
        return await self.bot.send_message(settings.bots.admin_id, 
                                           "Произошла критическая ошибка. \n"
                                            f"Описание ошибки: {self.event.exception}\n"
                                            f"Вызвана пользователем с ID: {user.id}\n"
                                            f"Полный лог сохранен в: {settings.bots.error_log}"
                                            )