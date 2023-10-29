import asyncio
from typing import Optional, Callable, Dict, List

import pyrogram
from pyrogram.filters import Filter

from ..config import config
from ..exceptions import ListenerTimeout, ListenerStopped
from ..types import ListenerTypes, Identifier, Listener
from ..utils import should_patch, patch_into


@patch_into(pyrogram.client.Client)
class Client(pyrogram.client.Client):
    listeners: Dict[ListenerTypes, List[Listener]]
    old__init__: Callable

    @should_patch()
    def __init__(self, *args, **kwargs):
        self.listeners = {listener_type: [] for listener_type in ListenerTypes}
        self.old__init__(*args, **kwargs)

    @should_patch()
    async def listen(
        self,
        filters: Optional[Filter] = None,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        timeout: Optional[int] = None,
        unallowed_click_alert: bool = True,
        chat_id: int = None,
        user_id: int = None,
        message_id: int = None,
        inline_message_id: str = None,
    ):
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

        loop = asyncio.get_event_loop()
        future = loop.create_future()
        future.add_done_callback(
            lambda f: self.stop_listening(
                listener_type,
                user_id=user_id,
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
            )
        )

        listener = Listener(
            future=future,
            filters=filters,
            unallowed_click_alert=unallowed_click_alert,
            identifier=pattern,
            listener_type=listener_type,
        )

        self.listeners[listener_type].append(listener)

        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.exceptions.TimeoutError:
            if callable(config.timeout_handler):
                config.timeout_handler(pattern, listener, timeout)
            elif config.throw_exceptions:
                raise ListenerTimeout(timeout)

    @should_patch()
    async def ask(
        self,
        chat_id: int,
        text: str,
        filters: Optional[Filter] = None,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        timeout: Optional[int] = None,
        unallowed_click_alert: bool = True,
        user_id: int = None,
        message_id: int = None,
        inline_message_id: str = None,
        *args,
        **kwargs,
    ):
        sent_message = None
        if text.strip() != "":
            sent_message = await self.send_message(chat_id, text, *args, **kwargs)

        response = await self.listen(
            filters=filters,
            listener_type=listener_type,
            timeout=timeout,
            unallowed_click_alert=unallowed_click_alert,
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
        if response:
            response.sent_message = sent_message

        return response

    @should_patch()
    def get_matching_listener(
        self, pattern: Identifier, listener_type: ListenerTypes
    ) -> Optional[Listener]:
        matching = []
        for listener in self.listeners[listener_type]:
            if listener.identifier.matches(pattern):
                matching.append(listener)

        # in case of multiple matching listeners, the most specific should be returned
        def count_populated_attributes(listener_item: Listener):
            return listener_item.identifier.count_populated()

        return max(matching, key=count_populated_attributes, default=None)

    @should_patch()
    def remove_listener(self, listener: Listener):
        self.listeners[listener.listener_type].remove(listener)

    @should_patch()
    def get_many_matching_listeners(
        self, pattern: Identifier, listener_type: ListenerTypes
    ) -> List[Listener]:
        listeners = []
        for listener in self.listeners[listener_type]:
            if listener.identifier.matches(pattern):
                listeners.append(listener)
        return listeners

    @should_patch()
    def stop_listening(
        self,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        chat_id: int = None,
        user_id: int = None,
        message_id: int = None,
        inline_message_id: str = None,
    ):
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
        listeners = self.get_many_matching_listeners(pattern, listener_type)

        for listener in listeners:
            self.remove_listener(listener)

            if listener.future.done():
                return

            if callable(config.stopped_handler):
                config.stopped_handler(pattern, listener)
            elif config.throw_exceptions:
                listener.future.set_exception(ListenerStopped())
