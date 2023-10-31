from types import SimpleNamespace

config = SimpleNamespace(
    timeout_handler=None,
    stopped_handler=None,
    throw_exceptions=True,
    unallowed_click_alert=True,
    unallowed_click_alert_text=("[pyromod] You're not expected to click this button."),
    disable_startup_logs=False,
)

__all__ = ["config"]
