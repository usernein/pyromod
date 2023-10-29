## Configuration

pyromod offers various configuration options to customize its behavior according to your specific needs. This guide will walk you through the process of configuring pyromod using the `pyromod.config` object.

This is completely optional though. You can use pyromod as normal without configuring it.

### Import the Configuration Object

Before you can start configuring pyromod, you need to import the `config` object:

```python
from pyromod.config import config
```

### Available Configuration Options

#### 1. Timeout Handler

The `timeout_handler` is an optional callback function that you can set to handle timeouts for listeners. If you want to define a custom function to handle timeouts, you can assign it to `config.timeout_handler`.

Example:

```python
## Set a custom timeout handler function
config.timeout_handler = my_custom_timeout_handler
```

#### 2. Stopped Handler

The `stopped_handler` is an optional callback function that you can set to handle events when a listener is stopped. You can assign a custom function to `config.stopped_handler` to define your stopped event handling.

Example:

```python
## Set a custom stopped handler function
config.stopped_handler = my_custom_stopped_handler
```

#### 3. Exception Handling

The `throw_exceptions` attribute is a boolean flag that determines whether pyromod should raise exceptions for certain events. You can set it to `True` or `False` based on your preferences.

Example:

```python
## Disable raising exceptions for listener events
config.throw_exceptions = False
```

#### 4. Unallowed Click Alert

The `unallowed_click_alert` is a boolean flag that controls whether users should be alerted when they click a button that doesn't match the filters. Setting it to `True` displays an alert, while `False` disables it.

Example:

```python
## Disable unallowed click alerts
config.unallowed_click_alert = False
```

#### 5. Custom Alert Text

When `unallowed_click_alert` is `True`, you can customize the alert text displayed to users. Set the `unallowed_click_alert_text` attribute to your desired text.

Example:

```python
## Set a custom alert text for unallowed clicks
config.unallowed_click_alert_text = "Unauthorized action: You cannot click this button."
```