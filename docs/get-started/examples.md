## Examples

**Awaiting a single message from a specific chat:**

```python
response = await client.listen(chat_id=chat_id)
```

**Awaiting a single message from a specific user in a specific chat:**

```python
response = await client.listen(chat_id=chat_id, user_id=user_id)
```

**Asking the user a question then await for the response:**

```python
response = await client.ask(chat_id=chat_id, text='What is your name?')
```

**Asking the user a question then await for the response, with a timeout:**

```python
try:
    response = await client.ask(chat_id=chat_id, text='What is your name?', timeout=10)
except ListenerTimeout:
    await message.reply('You took too long to answer.')
```

**Full handler example, getting user's name and age with bound method Chat.ask:**

```python
from pyromod import Client, Message
from pyrogram import filters


@Client.on_message(filters.command('form'))
async def on_form(client: Client, message: Message):
    chat = message.chat

    name = await chat.ask('What is your name?', filters=filters.text)
    age = await chat.ask('What is your age?', filters=filters.text)

    await message.reply(f'Your name is {name.text} and you are {age.text} years old.')
```

**Easier inline keyboard creation:**

```python
from pyromod.helpers import ikb

keyboard = ikb([
    [('Button 1', 'callback_data_1'), ('Button 2', 'callback_data_2')],
    [('Another button', 't.me/pyromodchat', 'url')]
])
```
