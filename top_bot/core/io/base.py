from aiogram.handlers import ErrorHandler, MessageHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent
from aiogram import Router, F
from top_bot.core.settings import settings
from aiogram.types.user import User

def base_dispatch(routers: list[Router]):
    for router in routers:
        router.errors.register(ProduceError)
        router.message.register(CancellingState, F.text.casefold()=="cancel")

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

class CancellingState(MessageHandler):
    async def handle(self, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return
        
        await state.clear()
        return await self.message.answer("Действие отменено.")
