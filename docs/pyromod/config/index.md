### *object* pyromod.config

The `config` object in Pyromod is a `SimpleNamespace` object that stores configuration settings for your Pyromod-powered
bot. These settings allow you to customize the behavior of your bot according to your specific needs.

* **Attributes:**
  * **timeout_handler:** An optional callback function that can be set to handle timeouts for listeners.
  * **stopped_handler:** An optional callback function that can be set to handle when a listener is stopped.
  * **throw_exceptions:** A boolean flag that determines whether Pyromod should raise exceptions for certain events.
  * **unallowed_click_alert:** A boolean flag that controls whether users should be alerted when they click a button that
  doesn't match the filters (i.e. clicking on a button that is supposed for other user to click).
  * **unallowed_click_alert_text:** The text to display in the alert when `unallowed_click_alert` is `True`.

* **Example Usage**

Here's an example of how to configure Pyromod using the `config` object:

```python
from pyromod.config import config

# Set a custom timeout handler function
config.timeout_handler = my_custom_timeout_handler

# Disable raising exceptions for listener events
config.throw_exceptions = False
```