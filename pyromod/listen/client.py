import asyncio
import uuid
from inspect import iscoroutinefunction
from types import SimpleNamespace
from typing import Optional, Callable, Dict, List, Union

import pyrogram
from pyrogram.filters import Filter

from ..config import config
from ..exceptions import ListenerTimeout, ListenerStopped
from ..types import ListenerTypes, Identifier, Listener
from ..utils import should_patch, patch_into

if not config.disable_startup_logs:
    print(
        "Pyromod is working! If you like pyromod, please star it at https://github.com/usernein/pyromod"
    )


@patch_into(pyrogram.client.Client)
class Client(pyrogram.client.Client):
    listeners: Dict[ListenerTypes, List[Listener]]
    messages_with_keyboard: Dict[str, SimpleNamespace]
    bot_client: pyrogram.Client = None
    bot_username: str = None
    old__init__: Callable

    @should_patch()
    def __init__(self, *args, **kwargs):
        self.listeners = {listener_type: [] for listener_type in ListenerTypes}
        self.messages_with_keyboard = {}
        self.old__init__(*args, **kwargs)

    @should_patch()
    async def listen(
            self,
            filters: Optional[Filter] = None,
            listener_type: ListenerTypes = ListenerTypes.MESSAGE,
            timeout: Optional[int] = None,
            unallowed_click_alert: bool = True,
            chat_id: Union[Union[int, str], List[Union[int, str]]] = None,
            user_id: Union[Union[int, str], List[Union[int, str]]] = None,
            message_id: Union[int, List[int]] = None,
            inline_message_id: Union[str, List[str]] = None,
    ):
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

        loop = asyncio.get_event_loop()
        future = loop.create_future()

        listener = Listener(
            future=future,
            filters=filters,
            unallowed_click_alert=unallowed_click_alert,
            identifier=pattern,
            listener_type=listener_type,
        )

        future.add_done_callback(lambda _future: self.remove_listener(listener))

        self.listeners[listener_type].append(listener)

        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.exceptions.TimeoutError:
            if callable(config.timeout_handler):
                if iscoroutinefunction(config.timeout_handler.__call__):
                    await config.timeout_handler(pattern, listener, timeout)
                else:
                    await self.loop.run_in_executor(
                        None, config.timeout_handler, pattern, listener, timeout
                    )
            elif config.throw_exceptions:
                raise ListenerTimeout(timeout)

    @should_patch()
    async def ask(
            self,
            chat_id: Union[Union[int, str], List[Union[int, str]]],
            text: str,
            filters: Optional[Filter] = None,
            listener_type: ListenerTypes = ListenerTypes.MESSAGE,
            timeout: Optional[int] = None,
            unallowed_click_alert: bool = True,
            user_id: Union[Union[int, str], List[Union[int, str]]] = None,
            message_id: Union[int, List[int]] = None,
            inline_message_id: Union[str, List[str]] = None,
            *args,
            **kwargs,
    ):
        sent_message = None
        if text.strip() != "":
            chat_to_ask = chat_id[0] if isinstance(chat_id, list) else chat_id
            sent_message = await self.send_message(chat_to_ask, text, *args, **kwargs)

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
    def remove_listener(self, listener: Listener):
        try:
            self.listeners[listener.listener_type].remove(listener)
        except ValueError:
            pass

    @should_patch()
    def get_listener_matching_with_data(
            self, data: Identifier, listener_type: ListenerTypes
    ) -> Optional[Listener]:
        matching = []
        for listener in self.listeners[listener_type]:
            if listener.identifier.matches(data):
                matching.append(listener)

        # in case of multiple matching listeners, the most specific should be returned
        def count_populated_attributes(listener_item: Listener):
            return listener_item.identifier.count_populated()

        return max(matching, key=count_populated_attributes, default=None)

    def get_listener_matching_with_identifier_pattern(
            self, pattern: Identifier, listener_type: ListenerTypes
    ) -> Optional[Listener]:
        matching = []
        for listener in self.listeners[listener_type]:
            if pattern.matches(listener.identifier):
                matching.append(listener)

        # in case of multiple matching listeners, the most specific should be returned

        def count_populated_attributes(listener_item: Listener):
            return listener_item.identifier.count_populated()

        return max(matching, key=count_populated_attributes, default=None)

    @should_patch()
    def get_many_listeners_matching_with_data(
            self,
            data: Identifier,
            listener_type: ListenerTypes,
    ) -> List[Listener]:
        listeners = []
        for listener in self.listeners[listener_type]:
            if listener.identifier.matches(data):
                listeners.append(listener)
        return listeners

    @should_patch()
    def get_many_listeners_matching_with_identifier_pattern(
            self,
            pattern: Identifier,
            listener_type: ListenerTypes,
    ) -> List[Listener]:
        listeners = []
        for listener in self.listeners[listener_type]:
            if pattern.matches(listener.identifier):
                listeners.append(listener)
        return listeners

    @should_patch()
    async def stop_listening(
            self,
            listener_type: ListenerTypes = ListenerTypes.MESSAGE,
            chat_id: Union[Union[int, str], List[Union[int, str]]] = None,
            user_id: Union[Union[int, str], List[Union[int, str]]] = None,
            message_id: Union[int, List[int]] = None,
            inline_message_id: Union[str, List[str]] = None,
    ):
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
        listeners = self.get_many_listeners_matching_with_identifier_pattern(pattern, listener_type)

        for listener in listeners:
            await self.stop_listener(listener)

    @should_patch()
    async def stop_listener(self, listener: Listener):
        self.remove_listener(listener)

        if listener.future.done():
            return

        if callable(config.stopped_handler):
            if iscoroutinefunction(config.stopped_handler.__call__):
                await config.stopped_handler(None, listener)
            else:
                await self.loop.run_in_executor(
                    None, config.stopped_handler, None, listener
                )
        elif config.throw_exceptions:
            listener.future.set_exception(ListenerStopped())

    @should_patch()
    def register_next_step_handler(
            self,
            callback: Callable,
            filters: Optional[Filter] = None,
            listener_type: ListenerTypes = ListenerTypes.MESSAGE,
            unallowed_click_alert: bool = True,
            chat_id: Union[Union[int, str], List[Union[int, str]]] = None,
            user_id: Union[Union[int, str], List[Union[int, str]]] = None,
            message_id: Union[int, List[int]] = None,
            inline_message_id: Union[str, List[str]] = None,
    ):
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

        listener = Listener(
            callback=callback,
            filters=filters,
            unallowed_click_alert=unallowed_click_alert,
            identifier=pattern,
            listener_type=listener_type,
        )

        self.listeners[listener_type].append(listener)

    async def inline_query_handler(self, _, query: pyrogram.types.InlineQuery):
        if not query.query.startswith("pyromod-get-keyboard-"):
            raise pyrogram.ContinuePropagation

        id = query.query.replace("pyromod-get-keyboard-", "")
        message: SimpleNamespace = self.messages_with_keyboard.get(id)

        if not message:
            print("Could not find message with keyboard with id", id)
            return

        results = [
            pyrogram.types.InlineQueryResultArticle(
                title="index",
                input_message_content=pyrogram.types.InputTextMessageContent(
                    message.text,
                    parse_mode=message.parse_mode,
                    entities=message.entities,
                    disable_web_page_preview=message.disable_web_page_preview,
                ),
                reply_markup=message.reply_markup,
            )
        ]

        await query.answer(results, cache_time=0)

        del self.messages_with_keyboard[id]

    @should_patch()
    async def setup_inline_bot(self, bot: pyrogram.Client):
        if not isinstance(bot, pyrogram.Client):
            raise TypeError("bot must be a pyrogram.Client instance")

        self.bot_client = bot
        bot_info = await bot.get_me()
        self.bot_username = bot_info.username

        handler = pyrogram.handlers.InlineQueryHandler(self.inline_query_handler,
                                                       filters=pyrogram.filters.regex(r"^pyromod-get-keyboard-"))
        bot.add_handler(handler, group=0)

    @should_patch()
    async def send_message(self, *args, **kwargs):
        if self == self.bot_client or "reply_markup" not in kwargs:
            return await self.oldsend_message(*args, **kwargs)

        reply_markup = kwargs["reply_markup"]
        del kwargs["reply_markup"]

        if not isinstance(reply_markup, pyrogram.types.InlineKeyboardMarkup):
            return await self.oldsend_message(*args, **kwargs)

        def get_from_args_or_kwargs(index: int, name: str, default=None):
            return args[index] if len(args) > index else kwargs.get(name, default)

        chat_id = get_from_args_or_kwargs(0, "chat_id", None)
        text = get_from_args_or_kwargs(1, "text", None)
        parse_mode = get_from_args_or_kwargs(2, "parse_mode", None)
        entities = get_from_args_or_kwargs(3, "entities", None)
        disable_web_page_preview = get_from_args_or_kwargs(4, "disable_web_page_preview", None)
        disable_notification = get_from_args_or_kwargs(5, "disable_notification", None)
        reply_to_message_id = get_from_args_or_kwargs(6, "reply_to_message_id", None)

        message = SimpleNamespace(
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
            entities=entities,
        )

        id = str(uuid.uuid4())
        id = id[:10]

        self.messages_with_keyboard[id] = message

        query = f"pyromod-get-keyboard-{id}"

        inline_results = await self.get_inline_bot_results(
            self.bot_username,
            query
        )
        result = inline_results.results[0]

        return await self.send_inline_bot_result(
            chat_id,
            inline_results.query_id,
            result.id,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
        )
