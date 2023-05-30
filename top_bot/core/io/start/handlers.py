from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.handlers import MessageHandler

def dispatch() -> Dispatcher:
    dp = Dispatcher(name="main")
    dp.message.register(Start, Command(commands="start"))
    return dp

class Start(MessageHandler):
    async def handle(self):
        arr = [1]
        arr[2]
        return await self.event.answer(
            "Привет! Я бот для Top Academy. \n"
            "Я создан для того, чтобы сохранять фотографии и другие материалы, которые сделали студенты. \n"
            "Подайте заявку для верификации вашим МУП:)"
                                            )