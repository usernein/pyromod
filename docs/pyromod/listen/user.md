### *class* pyromod.listen.User

Bases: `pyrogram.types.user_and_chats.user.User`

The `pyromod.listen.User` class is an extension of the `pyrogram.types.user_and_chats.user.User` class. It provides additional
methods for working with User objects with pyromod.

### *bound method* listen(*args, **kwargs):

Listen for a message or a callback query from the user. This method is a bound method that calls the `listen` method of
the `Client`
class, passing its own `User.id` as the `user_id` parameter.

**Parameters:**

* **args** - The arguments to pass to the `Client.listen` method.
* **kwargs** - The keyword arguments to pass to the `Client.listen` method.

**Returns:**
The message or callback query that was listened for.

### *bound method* ask(text: str, *args, **kwargs):

Sends a message with the specified text to the `User.id` as chat_id (i.e. user's private conversation) and wait for a
response from the user on the same chat. This method is a bound
method that calls
the `ask` method of the `Client` class, passing its own `User.id` as both `chat_id` and `user_id` parameters.

**Parameters:**

* **text** (*str*) – The text of the message to send.
* **args** - The arguments to pass to the `Client.ask` method.
* **kwargs** - The keyword arguments to pass to the `Client.ask` method.

**Returns:**
The message that was listened for. In the attribute `request`, you can find the Message object of the message that was
sent.

### *bound method* stop_listening()

Stop listening for messages and/or callback queries. This method is a bound method that calls the `stop_listening`
method
of the `Client` class, passing its own `User.id` as the `user_id` parameter.

**Returns:**
None
