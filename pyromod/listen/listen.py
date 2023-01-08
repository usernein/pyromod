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
from typing import Optional, Callable
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
        chat_id,
        user_id=None,
        filters=None,
        listener_type=ListenerTypes.MESSAGE,
        timeout=None,
        message_id=None,
    ):
        if type(listener_type) != ListenerTypes:
            raise TypeError(
                "Parameter listener_type should be a value from pyromod.listen.ListenerTypes"
            )

        future = loop.create_future()
        future.add_done_callback(
            functools.partial(self.stop_listening, chat_id, user_id)
        )

        self.futures[listener_type].update(
            {(chat_id, user_id, message_id): {"future": future, "filters": filters}}
        )

        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.exceptions.TimeoutError:
            if callable(PyromodConfig.timeout_handler):
                PyromodConfig.timeout_handler(chat_id, user_id, filters, timeout)
            elif PyromodConfig.throw_exceptions:
                raise ListenerTimeout(timeout)

    @patchable
    async def ask(
        self,
        chat_id,
        text,
        user_id=None,
        filters=None,
        listener_type=ListenerTypes.MESSAGE,
        timeout=None,
        *args,
        **kwargs
    ):
        request = await self.send_message(chat_id, text, *args, **kwargs)
        response = await self.listen(chat_id, user_id, filters, listener_type, timeout)
        response.request = request
        return response
    
    @patchable
    def get_listener(self, chat_id, user_id, message_id):
        
    @patchable
    def remove_future(self, unwanted_future):
        self.futures = {
            listener_type: {
                k: v for k, v in listener_array if v["future"] != unwanted_future
            }
            for listener_type, listener_array in self.futures.items()
        }

    @patchable
    def stop_listening(self, chat_id, user_id, listener_type=ListenerTypes.MESSAGE):
        listener = self.futures[listener_type].get((chat_id, user_id))

        if not listener:
            return
        elif listener["future"].done():
            self.remove_future(listener["future"])
            return

        if callable(PyromodConfig.canceled_handler):
            PyromodConfig.canceled_handler(chat_id, user_id)
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
            (message.chat.id, message.from_user.id)
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
