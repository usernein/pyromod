### *class* pyromod.listen.Chat

Bases: `pyrogram.types.user_and_chats.chat.Chat`

The `pyromod.listen.Chat` class is an extension of the `pyrogram.types.user_and_chats.chat.Chat` class. It provides additional
methods for working with chats with pyromod.

### *bound method* listen(*args, **kwargs):

Listen for a message or a callback query on the chat. This method is a bound method that calls the `listen` method of
the `Client`
class, passing its own `Chat.id` as the `chat_id` parameter.

**Parameters:**

* **args** - The arguments to pass to the `Client.listen` method.
* **kwargs** - The keyword arguments to pass to the `Client.listen` method.

**Returns:**
The message that was listened for.

### *bound method* ask(text: str, *args, **kwargs):

Sends a message with the specified text and wait for a response from the same chat. This method is a bound method that
calls
the `ask` method of the `Client` class, passing its own `Chat.id` as the `chat_id` parameter.

**Parameters:**

* **text** (*str*) – The text of the message to send.
* **args** - The arguments to pass to the `Client.ask` method.
* **kwargs** - The keyword arguments to pass to the `Client.ask` method.

**Returns:**
The message that was listened for. In the attribute `request`, you can find Message object of the message that was sent.

### *bound method* stop_listening()

Stop listening for messages and/or callback queries. This method is a bound method that calls the `stop_listening`
method
of the `Client` class, passing its own `Chat.id` as the `chat_id` parameter.

**Returns:**
None
