from typing import Callable

import pyrogram
from pyrogram.filters import Filter
from pyrogram.types import CallbackQuery

from .client import Client
from ..config import config
from ..types import ListenerTypes, Identifier, Listener
from ..utils import patch, patchable


@patch(pyrogram.handlers.callback_query_handler.CallbackQueryHandler)
class CallbackQueryHandler(pyrogram.handlers.callback_query_handler.CallbackQueryHandler):
    old__init__: Callable

    @patchable
    def __init__(self, callback: Callable, filters: Filter = None):
        self.original_callback = callback
        self.old__init__(self.resolve_future, filters)

    @patchable
    def compose_data_identifier(self, query: CallbackQuery):
        from_user = query.from_user
        message_id = query.message.id if query.message else None
        chat_id = query.message.chat.id if query.message else None
        from_user_id = from_user.id if from_user else None

        return Identifier(message_id=message_id, chat_id=chat_id, from_user_id=from_user_id,
                          inline_message_id=query.inline_message_id)

    @patchable
    async def check_if_has_matching_listener(self, client: Client, query: CallbackQuery) -> tuple[bool, Listener]:
        data = self.compose_data_identifier(query)

        listener = client.get_single_listener(data, ListenerTypes.MESSAGE)

        listener_does_match = False

        if listener:
            filters = listener.filters
            listener_does_match = (
                await filters(client, query) if callable(filters) else True
            )

        return listener_does_match, listener

    @patchable
    async def check(self, client: Client, query: CallbackQuery):
        listener_does_match, listener = await self.check_if_has_matching_listener(client, query)

        handler_does_match = (
            await self.filters(client, query)
            if callable(self.filters)
            else True
        )

        data = self.compose_data_identifier(query)

        if config.unallowed_click_alert:
            # matches with the current query but from any user
            permissive_identifier = Identifier(
                chat_id=data.chat_id,
                message_id=data.message_id,
                inline_message_id=data.inline_message_id,
                from_user_id=None,
            )

            matches = permissive_identifier.matches(data)

            if (matches and not listener_does_match) and listener.unallowed_click_alert:
                alert = (
                    listener.unallowed_click_alert
                    if isinstance(listener.unallowed_click_alert, str)
                    else config.unallowed_click_alert_text
                )
                await query.answer(alert)
                return False

        # let handler get the chance to handle if listener
        # exists but its filters doesn't match
        return listener_does_match or handler_does_match

    @patchable
    async def resolve_future(self, client: Client, query: CallbackQuery, *args):
        listener_does_match, listener = await self.check_if_has_matching_listener(client, query)

        if listener and not listener.future.done():
            listener.future.set_result(query)
            client.remove_listener(listener)
            raise pyrogram.StopPropagation
        else:
            await self.original_callback(client, query, *args)