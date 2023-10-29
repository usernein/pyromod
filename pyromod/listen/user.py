import pyrogram

from .client import Client
from ..utils import patch_into, should_patch


@patch_into(pyrogram.types.user_and_chats.user.User)
class User(pyrogram.types.user_and_chats.user.User):
    _client: Client

    @should_patch()
    def listen(self, *args, **kwargs):
        return self._client.listen(*args, user_id=self.id, **kwargs)

    @should_patch()
    def ask(self, text, *args, **kwargs):
        return self._client.ask(self.id, text, *args, user_id=self.id, **kwargs)

    @should_patch()
    def stop_listening(self, *args, **kwargs):
        return self._client.stop_listening(*args, user_id=self.id, **kwargs)
