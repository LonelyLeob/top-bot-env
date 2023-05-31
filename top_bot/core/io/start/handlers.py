from typing import Any
from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from top_bot.utils.keyboards import *
from top_bot.utils.callbacks import *
from top_bot.core.settings import settings

def dispatch() -> Dispatcher:
    dp = Dispatcher(name="main")
    dp.message.register(Start, Command(commands="start"))
    dp.callback_query.register(Apply, StartCallback.filter(F.action == 2))
    dp.callback_query.register(ProduceApply, StartCallback.filter(F.action.in_({0, 1})))
    dp.callback_query.register(SendTicket, StartCallback.filter(F.action==3))
    return dp

class Start(MessageHandler):
    async def handle(self):
        if self.from_user.id == settings.bots.manager_id:
            return await self.event.answer("Привет админ", reply_markup=ManagerInline().start(str(self.from_user.id)))
        elif self.from_user.id == "":
            return await self.event.answer("Привет препод", reply_markup=TeacherInline().start(str(self.from_user.id)))
        return await self.event.answer(
            "Привет! Я бот для Top Academy. \n"
            "Я создан для того, чтобы сохранять фотографии и другие материалы, которые сделали студенты. \n"
            "Подайте заявку для верификации вашим МУП:)",
                                            reply_markup=StartInline().start(self.from_user.id))
    
class Apply(CallbackQueryHandler):
    async def handle(self):
        cb = StartCallback.unpack(self.callback_data)
        return await self.bot.send_message(settings.bots.manager_id, f"Пользователь c никнеймом {self.from_user.full_name} отправил запрос, продолжить?", 
                                           reply_markup=ManagerInline().apply(cb.user))
    

class ProduceApply(CallbackQueryHandler):
    async def handle(self):
        cb = StartCallback.unpack(self.callback_data)
        if cb.action==0:
            return await self.bot.send_message(cb.user, "Ваш запрос подтвержден! Можете перейти к группам:)", reply_markup=TeacherInline().start(str(cb.user)))
        return await self.bot.send_message(cb.user, "Ваш запрос отклонен, обратитесь к МУП за разрешением вопроса.", reply_markup=StartInline().start(cb.user))

class SendTicket(CallbackQueryHandler):
    async def handle(self):
        await self.bot.send_message(settings.bots.admin_id, f"Тикет: {self.message.text}")
        return await self.bot.send_message(self.from_user.id, "Сообщение доставлено, скоро починим:)")