from typing import Callable

import pyrogram
from pyrogram.filters import Filter
from pyrogram.types import Message

from .client import Client
from ..types import ListenerTypes, Identifier
from ..utils import should_patch, patch_into


@patch_into(pyrogram.handlers.message_handler.MessageHandler)
class MessageHandler(pyrogram.handlers.message_handler.MessageHandler):
    filters: Filter
    old__init__: Callable

    @should_patch()
    def __init__(self, callback: Callable, filters: Filter = None):
        self.original_callback = callback
        self.old__init__(self.resolve_future, filters)

    @should_patch()
    async def check_if_has_matching_listener(self, client: Client, message: Message):
        from_user = message.from_user
        from_user_id = from_user.id if from_user else None

        message_id = getattr(message, "id", getattr(message, "message_id", None))

        data = Identifier(
            message_id=message_id, chat_id=message.chat.id, from_user_id=from_user_id
        )

        listener = client.get_matching_listener(data, ListenerTypes.MESSAGE)

        listener_does_match = False

        if listener:
            filters = listener.filters
            listener_does_match = (
                await filters(client, message) if callable(filters) else True
            )

        return listener_does_match, listener

    @should_patch()
    async def check(self, client: Client, message: Message):
        listener_does_match = (
            await self.check_if_has_matching_listener(client, message)
        )[0]

        handler_does_match = (
            await self.filters(client, message) if callable(self.filters) else True
        )

        # let handler get the chance to handle if listener
        # exists but its filters doesn't match
        return listener_does_match or handler_does_match

    @should_patch()
    async def resolve_future(self, client: Client, message: Message, *args):
        listener_does_match, listener = await self.check_if_has_matching_listener(
            client, message
        )

        if listener_does_match:
            if not listener.future.done():
                listener.future.set_result(message)
                client.remove_listener(listener)
                raise pyrogram.StopPropagation
        else:
            await self.original_callback(client, message, *args)
