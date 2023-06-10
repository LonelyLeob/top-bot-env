from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import TelegramObject, Message
from top_bot.core.service import Auth
from top_bot.utils.keyboards import StartInline
from aiogram import Bot

class AuthMiddleware(BaseMiddleware):
    bot: Bot
    
    def __init__(self) -> None:
        return super().__init__()

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]):
        id = data['event_from_user'].id
        if not (Auth.is_manager(id)) and (Auth.is_teacher(id)):
            await AuthMiddleware.bot.send_message(chat_id=id, text="Вас нет в списке пользователей. Подайте заявку", reply_markup=StartInline().start(id))
            raise Exception        
        else:
            return await handler(event, data)