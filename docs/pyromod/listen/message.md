### *class* pyromod.listen.Message

Bases: `pyrogram.Message`

The `pyromod.listen.Message` class is an extension of the `pyrogram.Message` class. It provides additional methods for waiting
for user clicks on inline buttons within messages.

### *async* wait_for_click(from_user_id: int | None = None, timeout: int | None = None, filters: Filter | None = None,

alert: str | bool = True)

Wait for a user to click any inline button within the message. This method is a shorthand bound method to
call `Client.listen` with `ListenerTypes.CALLBACK_QUERY` as the `listener_type`.

**Parameters:**

* **from_user_id** (*int* *or* *None*) – The user ID to wait for clicks from. If `None`, the method waits for clicks
  from any user.
* **timeout** (*int* *or* *None*) – The maximum amount of time to wait for a button click. If `None`, there is no
  timeout.
* **filters** (*pyrogram.filters.Filter* *or* *None*) – A filter to check the incoming click event against. Can be used
  to filter clicks by the button data.
* **alert** (*str* *or* *bool*) – The alert text to show to users whose ID does not match `from_user_id`. If `True`, the
  default alert text is shown. If `False`, no alert is shown.

**Returns:**
The CallbackQuery object of the button click.
