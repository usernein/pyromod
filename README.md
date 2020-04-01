# pyromod
A monkeypatcher add-on for Pyrogram

## Introduction
pyromod is a compilation of utils i developed for extend my personal use of Pyrogram. Then i started to use it and more bots and now i published it to make it easier to be installed in new projects.
It works *together* with pyrogram, this is *not* a fork nor modded version. It does monkey patching to add features to Pyrogram classes.

IMPORTANT: you should have installed asyncio pyrogram.

## Usage
Import `pyromod` at least one time in your script, so you'll be able to use modified pyrogram in all files of the same proccess. Example:
```python
# config.py
import pyromod.listen
from pyrogram import Client

app = Client('my_session')
```
```python
# any other .py
from config import app
# no need to import pyromod again, pyrogram is already monkeypatched globally (at the same proccess)
```

I separated the patches between packages to allow you to import only what you want. The `__init__.py` of each package does the monkeypatch automatically as soon as they are imported (except for `pyromod.helpers`, which provides classes and functions that should be explicitely imported).

### `pyromod.listen`
Just import it, it will automatically do the monkeypatch and you'll get these new methods:
- `await pyrogram.Client.listen(chat_id, filters=None, timeout=30)`
Awaits for a new message in the specified chat and returns it
You can pass Update Filters to the filters parameter just like you do for the update handlers. e.g. `filters=Filters.photo & Filters.bot`

- `await pyrogram.Client.ask(text, chat_id, filters=None, timeout=30)`
Same of `.listen()` above, but sends a message before awaiting
You can pass custom parameters to its send_message() call. Check the example below.

- The bound methods `Chat.listen`, `User.listen`, `Chat.ask` and `User.ask`

Example:
```python
from pyromod import listen # or import pyromod.listen
from pyrogram import Client
client = Client(...)
...
    answer = await client.ask(chat_id, '*Send me your name:*', parse_mode='Markdown')
    await client.send_message(chat_id, f'Your name is: {answer.text}')    
```

### `pyromod.filters`
Import it and the following Update Filters will be monkeypatched to `pyrogram.Filters`:

- `Filters.dice`
A dice message.

- `Filters.callback_regex(pattern, flags: int = 0)`
Same of `Filters.regex`, but for CallbackQuery updates
The CallbackQuery object will hold the matches on the new `CallbackQuery.matches` attribute (just like `Message.matches`)


### Copyright & License
This project may include snippets of Pyrogram code
- Pyrogram - Telegram MTProto API Client Library for Python. Copyright (C) 2017-2020 Dan <<https://github.com/delivrance>>

Licensed under the terms of the [GNU Lesser General Public License v3 or later (LGPLv3+)](COPYING.lesser)
