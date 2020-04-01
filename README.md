# pyromod
A monkeypatched add-on for Pyrogram

## Introduction
pyromod is a compilation of utils i developed for extend my personal use of Pyrogram. Then i started to use it and more bots and now i published it to make it easier to be installed in new projects.
It works *together* with pyrogram, this is *not* a fork nor modded version. It does monkey patching to add features to Pyrogram classes.
Note: it uses pyrogram asyncio.

## Usage
I separated the utils in packages, you should import them to do the monkeypatch (except for `pyromod.utils` with provides classes and functions to be explicitely imported):

### `pyromod.listen`
Just import it and you have these new methods:
- `await pyrogram.Client.listen(chat_id, timeout=30)`
Awaits for a new message in the specified chat and returns it

- `await pyrogram.Client.ask(text, chat_id, timeout=30)`
Same of `.listen()` above, but sends a message before awaiting

- The bound methods `Chat.listen`, `User.listen`, `Chat.ask` and `User.ask`

Usage:
```python
from pyromod import listen # or import pyromod.listen
from pyrogram import Client
client = Client(...)
...
answer = await client.ask('Confirm? [Yn]', chat_id)
```

### Copyright & License
This project may include snippets of Pyrogram code
- Pyrogram - Telegram MTProto API Client Library for Python
- Copyright (C) 2017-2020 Dan <<https://github.com/delivrance>>
- Licensed under the terms of the [GNU Lesser General Public License v3 or later (LGPLv3+)](COPYING.lesser)
