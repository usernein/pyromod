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
import functools
from typing import Optional, Callable, Any
import pyrogram

from enum import Enum
from ..utils import patch, patchable

loop = asyncio.get_event_loop()


class ListenerCanceled(Exception):
    pass


class ListenerTimeout(Exception):
    pass


class PyromodConfig:
    timeout_handler = None
    canceled_handler = None
    throw_exceptions = None


class Identifier(tuple):
    def __getattribute__(self, __name: str) -> Any:
        tuple_pos = {
            "chat_id": 0,
            "user_id": 1,
            "message_id": 2,
        }
        if __name not in tuple_pos:
            raise AttributeError(__name)

        pos = tuple_pos[__name]
        return self[0] if pos < len(self) else None


ListenerTypes = Enum("ListenerTypes", ["MESSAGE", "CALLBACK_QUERY"])


@patch(pyrogram.client.Client)
class Client:
    @patchable
    def __init__(self, *args, **kwargs):
        self.futures = {listener_type: {} for listener_type in ListenerTypes}
        self.old__init__(*args, **kwargs)

    @patchable
    async def listen(
        self,
        identifier: tuple,
        filters=None,
        listener_type=ListenerTypes.MESSAGE,
        timeout=None,
    ):
        if type(listener_type) != ListenerTypes:
            raise TypeError(
                "Parameter listener_type should be a"
                " value from pyromod.listen.ListenerTypes"
            )

        identifier = (
            Identifier(identifier) if type(identifier) == tuple else identifier
        )

        future = loop.create_future()
        future.add_done_callback(
            functools.partial(self.stop_listening, identifier)
        )

        self.futures[listener_type].update(
            {identifier: {"future": future, "filters": filters}}
        )

        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.exceptions.TimeoutError:
            if callable(PyromodConfig.timeout_handler):
                PyromodConfig.timeout_handler(identifier, filters, timeout)
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
        identifier = (
            Identifier(identifier) if type(identifier) == tuple else identifier
        )

        request = await self.send_message(
            identifier.chat_id, text, *args, **kwargs
        )
        response = await self.listen(
            identifier, filters, listener_type, timeout
        )
        response.request = request

        return response

    def match_listener(self, data):  # needed for matching when message_id or
        # user_id is null, and to take precedence
        data = Identifier(data)

        # case with 3 args on identifier
        # most probably waiting for a specific user
        # to click a button in a specific message
        if data in self.futures:
            return self.futures[data]

        # cases with 2 args on identifier
        # (None, user, message) does not make
        # sense since the message_id is not unique
        elif Identifier(data.chat_id, data.user_id, None) in self.futures:
            matched = Identifier(data.chat_id, data.user_id, None)
            return self.futures[matched]
        elif Identifier(data.chat_id, None, data.message_id) in self.futures:
            matched = Identifier(data.chat_id, None, data.message_id)
            return self.futures[matched]

        # cases with 1 arg on identifier
        # (None, None, message) does not make sense as well
        elif Identifier(data.chat_id, None, None) in self.futures:
            matched = Identifier(data.chat_id, None, None)
            return self.futures[matched]
        elif Identifier(None, data.user_id, None) in self.futures:
            matched = Identifier(None, data.user_id, None)
            return self.futures[matched]

    @patchable
    def remove_future(self, unwanted_future):
        self.futures = {
            listener_type: {
                k: v
                for k, v in listener_array
                if v["future"] != unwanted_future
            }
            for listener_type, listener_array in self.futures.items()
        }

    @patchable
    def stop_listening(
        self, identifier: tuple, listener_type=ListenerTypes.MESSAGE
    ):
        listener = self.futures[listener_type].get(identifier)

        if not listener:
            return
        elif listener["future"].done():
            self.remove_future(listener["future"])
            return

        if callable(PyromodConfig.canceled_handler):
            PyromodConfig.canceled_handler(identifier)
        elif PyromodConfig.throw_exceptions:
            listener["future"].set_exception(ListenerCanceled())

        self.remove_future(listener["future"])


@patch(pyrogram.handlers.message_handler.MessageHandler)
class MessageHandler:
    @patchable
    def __init__(self, callback: Callable, filters=None):
        self.registered_handler = callback
        self.old__init__(self.resolve_future, filters)

    @patchable
    async def check(self, client, message):
        listener = client.futures[ListenerTypes.MESSAGE].get(
            (message.chat.id, message.from_user.id, None)
        )
        filters = listener["filters"] if listener else self.filters

        return await filters(client, message) if callable(filters) else True

    @patchable
    async def resolve_future(self, client, message, *args):
        listener = client.futures[ListenerTypes.MESSAGE].get(
            (message.chat.id, message.from_user.id)
        )

        if listener and not listener["future"].done():
            listener["future"].set_result(message)
            client.remove_future(listener["future"])
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
        listener = client.futures[ListenerTypes.CALLBACK_QUERY].get(
            (query.message.chat.id, query.from_user.id)
        )
        filters = listener["filters"] if listener else self.filters

        return await filters(client, query) if callable(filters) else True

    @patchable
    async def resolve_future(self, client, query, *args):
        listener = client.futures[ListenerTypes.CALLBACK_QUERY].get(
            (query.message.chat.id, query.from_user.id)
        )

        if listener and not listener["future"].done():
            listener["future"].set_result(query)
            client.remove_future(listener["future"])
        else:
            await self.registered_handler(client, query, *args)


@patch(pyrogram.types.messages_and_media.message.Message)
class Message(pyrogram.types.messages_and_media.message.Message):
    @patchable
    async def wait_for_click(
        self, from_user_id: Optional[int], timeout: Optional[int], filters=None
    ):
        return await self._client.listen(
            self.chat.id,
            from_user_id,
            listener_type=ListenerTypes.CALLBACK_QUERY,
            message_id=self.id,
            timeout=timeout,
            filters=filters,
        )


@patch(pyrogram.types.user_and_chats.chat.Chat)
class Chat(pyrogram.types.Chat):
    @patchable
    def listen(self, *args, **kwargs):
        return self._client.listen(self.id, *args, **kwargs)

    @patchable
    def ask(self, *args, **kwargs):
        return self._client.ask(self.id, *args, **kwargs)

    @patchable
    def stop_listening(self):
        return self._client.stop_listening(self.id)


@patch(pyrogram.types.user_and_chats.user.User)
class User(pyrogram.types.User):
    @patchable
    def listen(self, *args, **kwargs):
        return self._client.listen(self.id, self.id, *args, **kwargs)

    @patchable
    def ask(self, *args, **kwargs):
        return self._client.ask(self.id, *args, user_id=self.id, **kwargs)

    @patchable
    def stop_listening(self):
        return self._client.stop_listening(self.id)
