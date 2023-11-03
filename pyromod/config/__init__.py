from types import SimpleNamespace

config = SimpleNamespace(
    timeout_handler=None,
    stopped_handler=None,
    throw_exceptions=True,
    unallowed_click_alert=True,
    unallowed_click_alert_text=("[pyromod] You're not expected to click this button."),
    disable_startup_logs=False,
)
"""
This is a config object that contains all the configuration variables that can be changed.

Attributes:
    timeout_handler (Callable): A function that will be called when a listener times out.
    stopped_handler (Callable): A function that will be called when a listener is stopped.
    throw_exceptions (bool): Whether to throw exceptions or not.
    unallowed_click_alert (bool): Whether to alert the user when they click a button that is not allowed.
    unallowed_click_alert_text (str): The text to send when the user clicks a button that is not allowed.
    disable_startup_logs (bool): Whether to disable the startup logs or not.
"""

__all__ = ["config"]
