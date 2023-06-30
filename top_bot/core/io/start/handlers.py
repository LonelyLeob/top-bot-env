from typing import Any
from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.handlers import MessageHandler, CallbackQueryHandler
from top_bot.core.service import Auth
from top_bot.utils.keyboards import *
from top_bot.utils.callbacks import *
from top_bot.core.settings import settings
from top_bot.core.io.start.middleware import AuthMiddleware
from aiogram.fsm.context import FSMContext

def dispatch() -> Dispatcher:
    dp = Dispatcher(name="main")
    #dp.message.middleware.register(AuthMiddleware())
    dp.message.register(Start, Command(commands="start"))
    dp.callback_query.register(Apply, StartCallback.filter(F.action == 2))
    dp.callback_query.register(ProduceApply, StartCallback.filter(F.action.in_({0, 1})))
    dp.callback_query.register(SendTicket, StartCallback.filter(F.action==3))
    return dp

class Start(MessageHandler):
    async def handle(self):       
        state: FSMContext = self.data["state"]
        if self.from_user.id == settings.bots.manager_id:
            return await self.event.answer("Здравствуй менеджер", reply_markup=ManagerInline().start())
        elif Auth.is_teacher(str(self.from_user.id)):
            return await self.event.answer('Здравствуй преподаватель', reply_markup=TeacherInline().start())
        else:
            return await self.event.answer(
                "Привет! Я бот для Top Academy. \n"
                "Я создан для того, чтобы сохранять фотографии и другие материалы, которые сделали студенты. \n"
                "Подайте заявку для верификации вашим МУП:)",
                                                reply_markup=StartInline().start(user=self.from_user.id))
    
class Apply(CallbackQueryHandler):
    async def handle(self):
        await self.message.delete()
        await self.bot.send_message(self.from_user.id, 'Вы подали заявку, её обработка может занять некоторое время')
        return await self.bot.send_message(settings.bots.manager_id, f"Пользователь c никнеймом {self.from_user.full_name} отправил запрос, продолжить?", 
                                           reply_markup=ManagerInline().apply(user=self.from_user.id))
    

class ProduceApply(CallbackQueryHandler):
    async def handle(self):
        cb = StartCallback.unpack(self.callback_data)
        await self.message.delete()
        if cb.action==0:
            if Auth.create_user(cb.user):
                return await self.bot.send_message(cb.user, "Ваш запрос подтвержден! Можете перейти к группам:)", reply_markup=TeacherInline().start())
            else:
                return await self.bot.send_message(cb.user, 'Произошла непредвиденная ошибка при регистрации. Обратитесь к системному администратору')
        return await self.bot.send_message(cb.user, "Ваш запрос отклонен, обратитесь к МУП за разрешением вопроса.", reply_markup=StartInline().start(user=cb.user))

class SendTicket(CallbackQueryHandler):
    async def handle(self):
        await self.message.delete()
        await self.bot.send_message(settings.bots.admin_id, f"Тикет: {self.message.text}")
        return await self.bot.send_message(self.from_user.id, "Сообщение доставлено, скоро починим:)")