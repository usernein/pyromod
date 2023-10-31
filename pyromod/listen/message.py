from typing import Optional, Union, List

import pyrogram

from .client import Client
from ..types import ListenerTypes
from ..utils import patch_into, should_patch


@patch_into(pyrogram.types.messages_and_media.message.Message)
class Message(pyrogram.types.messages_and_media.message.Message):
    _client = Client

    @should_patch()
    async def wait_for_click(
        self,
        from_user_id: Optional[Union[Union[int, str], List[Union[int, str]]]] = None,
        timeout: Optional[int] = None,
        filters=None,
        alert: Union[str, bool] = True,
    ):
        message_id = getattr(self, "id", getattr(self, "message_id", None))

        return await self._client.listen(
            listener_type=ListenerTypes.CALLBACK_QUERY,
            timeout=timeout,
            filters=filters,
            unallowed_click_alert=alert,
            chat_id=self.chat.id,
            user_id=from_user_id,
            message_id=message_id,
        )
