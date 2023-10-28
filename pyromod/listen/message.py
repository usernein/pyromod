from typing import Optional, Union

import pyrogram

from .client import Client
from ..types import ListenerTypes
from ..utils import patch, patchable


@patch(pyrogram.types.messages_and_media.message.Message)
class Message(pyrogram.types.messages_and_media.message.Message):
    _client = Client

    @patchable
    async def wait_for_click(
            self,
            from_user_id: Optional[int] = None,
            timeout: Optional[int] = None,
            filters=None,
            alert: Union[str, bool] = True,
    ):
        return await self._client.listen(
            listener_type=ListenerTypes.CALLBACK_QUERY,
            timeout=timeout,
            filters=filters,
            unallowed_click_alert=alert,
            chat_id=self.chat.id,
            user_id=from_user_id,
            message_id=self.id,
        )