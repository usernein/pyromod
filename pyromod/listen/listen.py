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
import pyrogram

from ..utils import patch, patchable

loop = asyncio.get_event_loop()
    
        
@patch(pyrogram.client.client.Client)
class Client():
    @patchable
    def __init__(self, *args, **kwargs):
        self.deferred_listeners = {}
        self.using_mod = True
        
        self.old__init__(*args, **kwargs)
    
    @patchable
    async def listen(self, chat_id, filters=None, timeout=30):
        chat = await self.get_chat(chat_id)
        chat_id = chat.id
        
        future = loop.create_future()
        future.add_done_callback(
            functools.partial(self.clearListener, chat_id)
        )
        self.deferred_listeners.update(
            {chat_id: {"future": future, "filters": filters}}
        )
        response = await asyncio.wait_for(future, timeout)
        return response
    
    @patchable
    async def ask(self, chat_id, text, filters=None, timeout=30, *args, **kwargs):
        request = await self.send_message(chat_id, text, *args, **kwargs)
        response = await self.listen(chat_id, filters, timeout)
        response.request = request
        return response
   
    @patchable
    def clearListener(self, chat_id, future):
        if future == self.deferred_listeners[chat_id]:
            self.deferred_listeners.pop(chat_id, None)
            
    __wraps__ = [__init__, listen, ask, clearListener]
            
@patch(pyrogram.client.handlers.message_handler.MessageHandler)
class MessageHandler():
    @patchable
    def __init__(self, callback: callable, filters=None):
        self.user_callback = callback
        self.old__init__(self.resolveListener, filters)
    
    @patchable
    async def resolveListener(self, client, message, *args):    
        future_exists = message.chat.id in client.deferred_listeners
        if future_exists and not client.deferred_listeners[message.chat.id]['future'].done():
            client.deferred_listeners[message.chat.id]['future'].set_result(message)
        else:
            if future_exists and client.deferred_listeners[message.chat.id]['future'].done():
                client.clearListener(message.chat.id, client.deferred_listeners[message.chat.id]['future'])
            await self.user_callback(client, message, *args)
    
    @patchable
    def check(self, update):
        client = update._client
        listener = client.deferred_listeners[update.chat.id] if update.chat.id in client.deferred_listeners else None
        if listener and not listener['future'].done() and (listener['filters'](update) if callable(listener['filters']) else True):
            return True
            
        return (
            self.filters(update)
            if callable(self.filters)
            else True
        )

@patch(pyrogram.client.types.user_and_chats.chat.Chat)
class Chat(pyrogram.Chat):
    @patchable
    def listen(self, *args, **kwargs):
        return self._client.listen(self.id, *args, **kwargs)
    @patchable
    def ask(self, *args, **kwargs):
        return self._client.ask(self.id, *args, **kwargs)

@patch(pyrogram.client.types.user_and_chats.user.User)
class User(pyrogram.User):
    @patchable
    def listen(self, *args, **kwargs):
        return self._client.listen(self.id, *args, **kwargs)
    @patchable
    def ask(self, *args, **kwargs):
        return self._client.ask(self.id, *args, **kwargs)
        