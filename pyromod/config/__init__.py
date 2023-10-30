from types import SimpleNamespace
from typing import Callable

config = SimpleNamespace(
    timeout_handler: Callable = None,
    stopped_handler: Callable = None,
    throw_exceptions: bool = True,
    unallowed_click_alert: bool = True,
    unallowed_click_alert_text: str = ("[pyromod] You're not expected to click this button."),
)

__all__ = ["config"]
