"""
pyromod - A monkeypatcher add-on for Pyrogram
Copyright (C) 2020 Cezar H. <https://github.com/usernein>

This file is part of pyromod.

pyromod is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyromod is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyromod.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
from typing import Optional, Callable, Union
import pyrogram
from enum import Enum
from ..utils import patch, patchable, PyromodConfig

loop = asyncio.get_event_loop()


class ListenerStopped(Exception):
    pass


class ListenerTimeout(Exception):
    pass


class ListenerTypes(Enum):
    MESSAGE = "message"
    CALLBACK_QUERY = "callback_query"


@patch(pyrogram.client.Client)
class Client:
    @patchable
    def __init__(self, *args, **kwargs):
        self.listeners = {listener_type: {} for listener_type in ListenerTypes}
        self.old__init__(*args, **kwargs)

    @patchable
    async def listen(
        self,
        identifier: tuple,
        filters=None,
        listener_type=ListenerTypes.MESSAGE,
        timeout=None,
        unallowed_click_alert=True,
    ):
        if type(listener_type) != ListenerTypes:
            raise TypeError(
                "Parameter listener_type should be a"
                " value from pyromod.listen.ListenerTypes"
            )

        future = loop.create_future()
        future.add_done_callback(
            lambda f: self.stop_listening(identifier, listener_type)
        )

        listener_data = {
            "future": future,
            "filters": filters,
            "unallowed_click_alert": unallowed_click_alert,
        }

        self.listeners[listener_type].update({identifier: listener_data})

        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.exceptions.TimeoutError:
            if callable(PyromodConfig.timeout_handler):
                PyromodConfig.timeout_handler(
                    identifier, listener_data, timeout
                )
            elif PyromodConfig.throw_exceptions:
                raise ListenerTimeout(timeout)

    @patchable
    async def ask(
        self,
        text,
        identifier: tuple,
        filters=None,
        listener_type=ListenerTypes.MESSAGE,
        timeout=None,
        *args,
        **kwargs
    ):
        request = await self.send_message(identifier[0], text, *args, **kwargs)
        response = await self.listen(
            identifier, filters, listener_type, timeout
        )
        if response:
            response.request = request

        return response

    """
    needed for matching when message_id or
    user_id is null, and to take precedence
    """

    @patchable
    def match_listener(
        self,
        data: Optional[tuple] = None,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        identifier_pattern: Optional[tuple] = None,
    ) -> tuple:
        if data:
            listeners = self.listeners[listener_type]
            # case with 3 args on identifier
            # most probably waiting for a specific user
            # to click a button in a specific message
            if data in listeners:
                return listeners[data], data

            # cases with 2 args on identifier
            # (None, user, message) does not make
            # sense since the message_id is not unique
            elif (data[0], data[1], None) in listeners:
                matched = (data[0], data[1], None)
            elif (data[0], None, data[2]) in listeners:
                matched = (data[0], None, data[2])

            # cases with 1 arg on identifier
            # (None, None, message) does not make sense as well
            elif (data[0], None, None) in listeners:
                matched = (data[0], None, None)
            elif (None, data[1], None) in listeners:
                matched = (None, data[1], None)
            else:
                return None, None

            return listeners[matched], matched
        elif identifier_pattern:

            def match_identifier(pattern, identifier):
                comparison = (
                    pattern[0] in (identifier[0], None),
                    pattern[1] in (identifier[1], None),
                    pattern[2] in (identifier[2], None),
                )
                return comparison == (True, True, True)

            for identifier, listener in self.listeners[listener_type].items():
                if match_identifier(identifier_pattern, identifier):
                    return listener, identifier
            return None, None

    @patchable
    def stop_listening(
        self,
        data: Optional[tuple] = None,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        identifier_pattern: Optional[tuple] = None,
    ):
        listener, identifier = self.match_listener(
            data, listener_type, identifier_pattern
        )

        if not listener:
            return
        elif listener["future"].done():
            del self.listeners[listener_type][identifier]
            return

        if callable(PyromodConfig.stopped_handler):
            PyromodConfig.stopped_handler(identifier, listener)
        elif PyromodConfig.throw_exceptions:
            listener["future"].set_exception(ListenerStopped())

        del self.listeners[listener_type][identifier]


@patch(pyrogram.handlers.message_handler.MessageHandler)
class MessageHandler:
    @patchable
    def __init__(self, callback: Callable, filters=None):
        self.registered_handler = callback
        self.old__init__(self.resolve_future, filters)

    @patchable
    async def check(self, client, message):
        listener = client.match_listener(
            (message.chat.id, message.from_user.id, message.id),
            ListenerTypes.MESSAGE,
        )[0]

        listener_does_match = handler_does_match = False

        if listener:
            filters = listener["filters"]
            listener_does_match = (
                await filters(client, message) if callable(filters) else True
            )
        handler_does_match = (
            await self.filters(client, message)
            if callable(self.filters)
            else True
        )

        # let handler get the chance to handle if listener
        # exists but its filters doesn't match
        return listener_does_match or handler_does_match

    @patchable
    async def resolve_future(self, client, message, *args):
        listener_type = ListenerTypes.MESSAGE
        listener, identifier = client.match_listener(
            (message.chat.id, message.from_user.id, message.id),
            listener_type,
        )
        listener_does_match = False
        if listener:
            filters = listener["filters"]
            listener_does_match = (
                await filters(client, message) if callable(filters) else True
            )

        if listener_does_match:
            if not listener["future"].done():
                listener["future"].set_result(message)
                del client.listeners[listener_type][identifier]
                raise pyrogram.StopPropagation
        else:
            await self.registered_handler(client, message, *args)


@patch(pyrogram.handlers.callback_query_handler.CallbackQueryHandler)
class CallbackQueryHandler:
    @patchable
    def __init__(self, callback: Callable, filters=None):
        self.registered_handler = callback
        self.old__init__(self.resolve_future, filters)

    @patchable
    async def check(self, client, query):
        listener = client.match_listener(
            (query.message.chat.id, query.from_user.id, query.message.id),
            ListenerTypes.CALLBACK_QUERY,
        )[0]

        # managing unallowed user clicks
        if PyromodConfig.unallowed_click_alert:
            permissive_listener = client.match_listener(
                identifier_pattern=(
                    query.message.chat.id,
                    None,
                    query.message.id,
                ),
                listener_type=ListenerTypes.CALLBACK_QUERY,
            )[0]

            if (permissive_listener and not listener) and permissive_listener[
                "unallowed_click_alert"
            ]:
                alert = (
                    permissive_listener["unallowed_click_alert"]
                    if type(permissive_listener["unallowed_click_alert"])
                    == str
                    else PyromodConfig.unallowed_click_alert_text
                )
                await query.answer(alert)
                return False

        filters = listener["filters"] if listener else self.filters

        return await filters(client, query) if callable(filters) else True

    @patchable
    async def resolve_future(self, client, query, *args):
        listener_type = ListenerTypes.CALLBACK_QUERY
        listener, identifier = client.match_listener(
            (query.message.chat.id, query.from_user.id, query.message.id),
            listener_type,
        )

        if listener and not listener["future"].done():
            listener["future"].set_result(query)
            del client.listeners[listener_type][identifier]
        else:
            await self.registered_handler(client, query, *args)


@patch(pyrogram.types.messages_and_media.message.Message)
class Message(pyrogram.types.messages_and_media.message.Message):
    @patchable
    async def wait_for_click(
        self,
        from_user_id: Optional[int] = None,
        timeout: Optional[int] = None,
        filters=None,
        alert: Union[str, bool] = True,
    ):
        return await self._client.listen(
            (self.chat.id, from_user_id, self.id),
            listener_type=ListenerTypes.CALLBACK_QUERY,
            timeout=timeout,
            filters=filters,
            unallowed_click_alert=alert,
        )


@patch(pyrogram.types.user_and_chats.chat.Chat)
class Chat(pyrogram.types.Chat):
    @patchable
    def listen(self, *args, **kwargs):
        return self._client.listen((self.id, None, None), *args, **kwargs)

    @patchable
    def ask(self, text, *args, **kwargs):
        return self._client.ask(text, (self.id, None, None), *args, **kwargs)

    @patchable
    def stop_listening(self, *args, **kwargs):
        return self._client.stop_listening(
            *args, identifier_pattern=(self.id, None, None), **kwargs
        )


@patch(pyrogram.types.user_and_chats.user.User)
class User(pyrogram.types.User):
    @patchable
    def listen(self, *args, **kwargs):
        return self._client.listen((None, self.id, None), *args, **kwargs)

    @patchable
    def ask(self, text, *args, **kwargs):
        return self._client.ask(
            text, (self.id, self.id, None), *args, **kwargs
        )

    @patchable
    def stop_listening(self, *args, **kwargs):
        return self._client.stop_listening(
            *args, identifier_pattern=(None, self.id, None), **kwargs
        )
