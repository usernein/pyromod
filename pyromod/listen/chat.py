import pyrogram

from .client import Client
from ..utils import patch_into, should_patch


@patch_into(pyrogram.types.user_and_chats.chat.Chat)
class Chat(pyrogram.types.user_and_chats.chat.Chat):
    _client: Client

    @should_patch()
    def listen(self, *args, **kwargs):
        """
        Listens for messages in the chat. Calls Client.listen() with the chat_id set to the chat's id.

        :param args: Arguments to pass to Client.listen().
        :param kwargs: Keyword arguments to pass to Client.listen().
        :return: The return value of Client.listen().
        """
        return self._client.listen(*args, chat_id=self.id, **kwargs)

    @should_patch()
    def ask(self, text, *args, **kwargs):
        """
        Asks a question in the chat. Calls Client.ask() with the chat_id set to the chat's id.
        :param text: The text to send.
        :param args: Arguments to pass to Client.ask().
        :param kwargs: Keyword arguments to pass to Client.ask().
        :return: The return value of Client.ask().
        """
        return self._client.ask(self.id, text, *args, **kwargs)

    @should_patch()
    def stop_listening(self, *args, **kwargs):
        """
        Stops listening for messages in the chat. Calls Client.stop_listening() with the chat_id set to the chat's id.

        :param args: Arguments to pass to Client.stop_listening().
        :param kwargs: Keyword arguments to pass to Client.stop_listening().
        :return: The return value of Client.stop_listening().
        """
        return self._client.stop_listening(*args, chat_id=self.id, **kwargs)
