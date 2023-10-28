import pyrogram

from .client import Client
from ..utils import patch, patchable


@patch(pyrogram.types.user_and_chats.chat.Chat)
class Chat(pyrogram.types.user_and_chats.chat.Chat):
    _client: Client

    @patchable
    def listen(self, *args, **kwargs):
        return self._client.listen(*args, chat_id=self.id, **kwargs)

    @patchable
    def ask(self, text, *args, **kwargs):
        return self._client.ask(text, *args, chat_id=self.id, **kwargs)

    @patchable
    def stop_listening(self, *args, **kwargs):
        return self._client.stop_listening(
            *args, chat_id=self.id, **kwargs
        )
