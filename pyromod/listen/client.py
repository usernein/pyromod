import asyncio
from inspect import iscoroutinefunction
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
    """
    A subclass of :class:`pyrogram.Client` with added functionality.

    This class is patched into :class:`pyrogram.Client` at runtime.
    """

    listeners: Dict[ListenerTypes, List[Listener]]
    """
    A dictionary of all listeners registered on this client. The keys are :class:`pyromod.types.ListenerTypes`
    and the values are lists of :class:`pyromod.types.Listener`.
    """

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
        chat_id: Union[Union[int, str], List[Union[int, str]]] = None,
        user_id: Union[Union[int, str], List[Union[int, str]]] = None,
        message_id: Union[int, List[int]] = None,
        inline_message_id: Union[str, List[str]] = None,
    ):
        """
        Creates a listener and waits for it to be fulfilled.

        :param filters: A filter to check if the listener should be fulfilled.
        :param listener_type: The type of listener to create. Defaults to :attr:`pyromod.types.ListenerTypes.MESSAGE`.
        :param timeout: The maximum amount of time to wait for the listener to be fulfilled. Defaults to ``None``.
        :param unallowed_click_alert: Whether to alert the user if they click on a button that is not intended for them. Defaults to ``True``.
        :param chat_id: The chat ID(s) to listen for. Defaults to ``None``.
        :param user_id: The user ID(s) to listen for. Defaults to ``None``.
        :param message_id: The message ID(s) to listen for. Defaults to ``None``.
        :param inline_message_id: The inline message ID(s) to listen for. Defaults to ``None``.
        :return: The Message or CallbackQuery that fulfilled the listener.
        """
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
        """
        Sends a message and waits for a response.

        :param chat_id: The chat ID(s) to wait for a message from. The first chat ID will be used to send the message.
        :param text: The text to send.
        :param filters: Same as :meth:`pyromod.types.Client.listen`.
        :param listener_type: Same as :meth:`pyromod.types.Client.listen`.
        :param timeout: Same as :meth:`pyromod.types.Client.listen`.
        :param unallowed_click_alert: Same as :meth:`pyromod.types.Client.listen`.
        :param user_id: Same as :meth:`pyromod.types.Client.listen`.
        :param message_id: Same as :meth:`pyromod.types.Client.listen`.
        :param inline_message_id: Same as :meth:`pyromod.types.Client.listen`.
        :param args: Additional arguments to pass to :meth:`pyrogram.Client.send_message`.
        :param kwargs: Additional keyword arguments to pass to :meth:`pyrogram.Client.send_message`.
        :return:
            Same as :meth:`pyromod.types.Client.listen`. The sent message is returned as the attribute ``sent_message``.
        """
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
        """
        Removes a listener from the :meth:`pyromod.types.Client.listeners` dictionary.

        :param listener: The listener to remove.
        :return: ``void``
        """
        try:
            self.listeners[listener.listener_type].remove(listener)
        except ValueError:
            pass

    @should_patch()
    def get_listener_matching_with_data(
        self, data: Identifier, listener_type: ListenerTypes
    ) -> Optional[Listener]:
        """
        Gets a listener that matches the given data.

        :param data: A :class:`pyromod.types.Identifier` to match against.
        :param listener_type: The type of listener to get. Must be a value from :class:`pyromod.types.ListenerTypes`.
        :return: The listener that matches the given data or ``None`` if no listener matches.
        """
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
        """
        Gets a listener that matches the given identifier pattern.

        The difference from :meth:`pyromod.types.Client.get_listener_matching_with_data` is that this method
        intends to get a listener by passing partial info of the listener identifier, while the other method
        intends to get a listener by passing the full info of the update data, which the listener should match with.

        :param pattern: A :class:`pyromod.types.Identifier` to match against.
        :param listener_type: The type of listener to get. Must be a value from :class:`pyromod.types.ListenerTypes`.
        :return: The listener that matches the given identifier pattern or ``None`` if no listener matches.
        """
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
        """
        Same of :meth:`pyromod.types.Client.get_listener_matching_with_data` but returns a list of listeners instead of one.

        :param data: Same as :meth:`pyromod.types.Client.get_listener_matching_with_data`.
        :param listener_type: Same as :meth:`pyromod.types.Client.get_listener_matching_with_data`.
        :return: A list of listeners that match the given data.
        """
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
        """
        Same of :meth:`pyromod.types.Client.get_listener_matching_with_identifier_pattern` but returns a list of listeners instead of one.

        :param pattern: Same as :meth:`pyromod.types.Client.get_listener_matching_with_identifier_pattern`.
        :param listener_type: Same as :meth:`pyromod.types.Client.get_listener_matching_with_identifier_pattern`.
        :return: A list of listeners that match the given identifier pattern.
        """
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
        """
        Stops all listeners that match the given identifier pattern.
        Uses :meth:`pyromod.types.Client.get_many_listeners_matching_with_identifier_pattern`.

        :param listener_type: The type of listener to stop. Must be a value from :class:`pyromod.types.ListenerTypes`.
        :param chat_id: The chat_id to match against.
        :param user_id: The user_id to match against.
        :param message_id: The message_id to match against.
        :param inline_message_id: The inline_message_id to match against.
        :return: ``void``
        """
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )
        listeners = self.get_many_listeners_matching_with_identifier_pattern(
            pattern, listener_type, match_against_pattern=True
        )

        for listener in listeners:
            await self.stop_listener(listener)

    @should_patch()
    async def stop_listener(self, listener: Listener):
        """
        Stops a listener, calling stopped_handler if applicable or raising ListenerStopped if throw_exceptions is True.

        :param listener: The :class:`pyromod.types.Listener` to stop.
        :return: ``void``
        :raises ListenerStopped: If throw_exceptions is True.
        """
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
        """
        Registers a listener with a callback to be called when the listener is fulfilled.

        :param callback: The callback to call when the listener is fulfilled.
        :param filters: Same as :meth:`pyromod.types.Client.listen`.
        :param listener_type: Same as :meth:`pyromod.types.Client.listen`.
        :param unallowed_click_alert: Same as :meth:`pyromod.types.Client.listen`.
        :param chat_id: Same as :meth:`pyromod.types.Client.listen`.
        :param user_id: Same as :meth:`pyromod.types.Client.listen`.
        :param message_id: Same as :meth:`pyromod.types.Client.listen`.
        :param inline_message_id: Same as :meth:`pyromod.types.Client.listen`.
        :return: ``void``
        """
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
