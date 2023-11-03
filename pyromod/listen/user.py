import pyrogram

from .client import Client
from ..utils import patch_into, should_patch


@patch_into(pyrogram.types.user_and_chats.user.User)
class User(pyrogram.types.user_and_chats.user.User):
    _client: Client

    @should_patch()
    def listen(self, *args, **kwargs):
        """
        Listens for messages from the user. Calls Client.listen() with the user_id set to the user's id.

        :param args: Arguments to pass to Client.listen().
        :param kwargs: Keyword arguments to pass to Client.listen().
        :return: The return value of Client.listen().
        """
        return self._client.listen(*args, user_id=self.id, **kwargs)

    @should_patch()
    def ask(self, text, *args, **kwargs):
        """
        Asks a question to the user. Calls Client.ask() with both chat_id and user_id set to the user's id.

        :param text: The text to send.
        :param args: Arguments to pass to Client.ask().
        :param kwargs: Keyword arguments to pass to Client.ask().
        :return: The return value of Client.ask().
        """
        return self._client.ask(self.id, text, *args, user_id=self.id, **kwargs)

    @should_patch()
    def stop_listening(self, *args, **kwargs):
        """
        Stops listening for messages from the user. Calls Client.stop_listening() with the user_id set to the user's id.

        :param args: Arguments to pass to Client.stop_listening().
        :param kwargs: Keyword arguments to pass to Client.stop_listening().
        :return: The return value of Client.stop_listening().
        """
        return self._client.stop_listening(*args, user_id=self.id, **kwargs)
