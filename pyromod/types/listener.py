from asyncio import Future
from dataclasses import dataclass

from pyrogram.filters import Filter

from .identifier import Identifier
from .listener_types import ListenerTypes


@dataclass
class Listener:
    listener_type: ListenerTypes
    future: Future
    filters: Filter
    unallowed_click_alert: bool
    identifier: Identifier
