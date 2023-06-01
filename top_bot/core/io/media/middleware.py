from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
import asyncio
from aiogram.types import Message, TelegramObject

class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data={}

    def __init__(self, latency=0.01) -> None:
        self.latency = latency

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not event.media_group_id:
            try:
                self.album_data["0"].append(event)
            except KeyError:
                self.album_data["0"] = [event]
                data["album"] = self.album_data["0"]
                del self.album_data["0"]
            return await handler(event, data)
        try:
            self.album_data[event.media_group_id].append(event)
        except KeyError:
            self.album_data[event.media_group_id] = [event]
            await asyncio.sleep(self.latency)

            data['_is_last'] = True
            data["album"] = self.album_data[event.media_group_id]
            return await handler(event, data)

        if event.media_group_id and data.get("_is_last"):
            del self.album_data[event.media_group_id]
            del data['_is_last']