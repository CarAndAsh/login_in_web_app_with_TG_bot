from typing import Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class DeleteUserMessageMiddleware(BaseMiddleware):
    id_dict:dict = {}


    async def __delete_prev_chat_message__(self, event, owner_id) -> None:
        if del_msg_id := self.id_dict.get(owner_id):
            await event.chat.delete_message(message_id=del_msg_id)


    async def  __call__(
            self,
            handler: Callable[[Message, dict[str, Any]],Awaitable[Any]],
            event: Message,
            data: dict[str, Any],
) -> Message:

        out_msg: Message = await handler(event, data)
        if isinstance(out_msg, Message):
            user_id: int = event.from_user.id
            await self.__delete_prev_chat_message__(event, event.bot.id)
            self.id_dict[user_id] = event.message_id
            await self.__delete_prev_chat_message__(event, user_id)
            self.id_dict[out_msg.from_user.id] = out_msg.message_id
            return out_msg
