### *class* pyromod.types.Listener

The `pyromod.types.Listener` class is designed to manage and handle different types of listeners used in pyromod. It enables
you to wait for specific events like messages or callback queries and provides mechanisms for defining the conditions
and filters that trigger these listeners.

### *Parameters:*

- **listener_type** (*pyromod.types.ListenerTypes*) – The type of listener that specifies the event you want to listen for. It
  can be either a "message" or a "callback_query."

- **future** (*asyncio.Future*) – A `Future` object representing the asynchronous task that waits for the event. When
  the event occurs, the `Future` will be resolved, and the listener will be able to proceed.

- **filters** (*pyrogram.filters.Filter*) – A filter to check the incoming event against. The listener will only be
  triggered when the event matches the provided filter.

- **unallowed_click_alert** (*bool*) – A flag that determines whether to send an alert if a button click event doesn't
  match the filter conditions. Setting this to `True` will send an alert message to the user in such cases.

- **identifier** (*pyromod.Identifier*) – An `Identifier` instance that defines the criteria for the event. It includes
  properties like `chat_id`, `message_id`, `from_user_id`, and `inline_message_id` that you want to match against the
  incoming event.
