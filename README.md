# pyromod
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/pyromodchat)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/usernein/pyromod)
![GitHub commits since latest release (by date) for a branch](https://img.shields.io/github/commits-since/usernein/pyromod/latest)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyromod?color=388E3C)

A monkeypatcher add-on for Pyrogram which does conversation handling and other cool stuff.

In other words, it is a compilation of utilities i developed for improving my personal experience with Pyrogram.
It works **together** with Pyrogram, it is **not** a fork/modded version. It does monkeypatching to add features to Pyrogram classes on the go (so i don't need to update on every Pyrogram's release).

## Usage
Import `pyromod` one time in your script and you'll already be able to use the modified pyrogram in all your handlers. Example:
```python
# config.py
import pyromod
from pyrogram import Client

app = Client('my_session')
```

Then you can, from another file, do `from config import app` to import the modded Pyrogram Client we created above. It will be modded globally.

All the patches are applied automatically as soon as pyromod is imported.

## Methods
All pyromod methods are callable by any of these ways:
- `await Client.<method>(identifier, ...)`
- `await Chat.<method>()`
- `await User.<method>()`

In the last two, Pyrogram automatically gets the ids from the object, to compound the `identifier` tuple that `Client.listen` uses.

These are the methods pyromod adds:
- `listen(identifier, filters=None, listener_type=ListenerTypes.MESSAGE, timeout=None, unallowed_click_alert=True)`
Awaits for a new message in the specified chat and returns its Message object. If listener_type is set to `ListenerTypes.CALLBACK_QUERY`, it awaits and returns a CallbackQuery object.
You can pass Update Filters to the `filters` parameter just like you do for the update handlers. e.g. `filters=filters.photo & filters.bot`
`identifier` is a tuple containing, in this exact order, (chat_id, user_id, message_id). It lets you specify exactly which update you want. You don't need to worry about that if you mostly use the bound methods.
`unnalowed_click_alert` is the text that users will see in an alert when the button is not waiting for them to click. If True, it uses the default text at `PyromodConfig.unnalowed_click_alert_text`. If False, no text is shown.

- `ask(text, identifier, filters=None, listener_type=ListenerTypes.MESSAGE, timeout=None, unallowed_click_alert=True)`
Same as `listen`, but sends a message to identifier[0] before and only then waits for a response.
You can additionally pass any of the `Client.send_message()` parameters. Check the example below.
The object of the sent message is returned inside of the attribute `request`

Example:
```python
answer = await message.chat.ask('*Send me your name:*', parse_mode=enums.ParseMode.MARKDOWN)
await answer.request.edit_text("Name received!")
await answer.reply(f'Your name is: {answer.text}', quote=True)    
```

- `Message.wait_for_click(from_user_id=None, timeout=None, filters=None, alert=True)`
Awaits from a click on any button on the Message object. If `from_user_id` is passed, pyromod will wait for a click of that user.
If you pass any text to `alert`, it will be shown to any other user. If `alert` is True, it will use the default text. If False, no text will be shown.

## `pyromod.helpers`
Tools for creating inline keyboards a lot easier.

### `pyromod.helpers.ikb`

Creates a inline keyboard.
Its first and only argument is a list (the keyboard itself) containing lists (the lines) of buttons, which can be lists or tuples. I use tuples to avoid a mess with a lot of brackets. Tuples makes it easier to read.

The button syntax is very simple: `(TEXT, VALUE, TYPE)`, with TYPE being any existent button type (e.g. `url`) and VALUE is its value. If you omit the type, it will be considered as a callback button.
If you pass only a string as button, it will be used as text and callback_data for the InlineKeyboardButton.
This syntax will be automagically converted by pyromod.

Examples:
```python
from pyromod.helpers import ikb
...
keyboard = ikb([
    [('Button 1', 'call_1'), ('Button 2', 'call_2')],
    [('Another button', 't.me/pyromodchat', 'url')]
])
await message.reply('Easy inline keyboard', reply_markup=keyboard)
```

```python
keyboard = ikb([
	["Mars", "Earth", "Venus"],
	["Saturn", "Jupyter"]
])
await message.reply("Easiest inline keyboard", reply_markup=keyboard)
```

- `pyromod.helpers.array_chunk`
Chunk the elements of a list into small lists. i.e. [1, 2, 3, 4] can become [[1,2], [3,4]]. This is extremely useful if you want to build a keyboard dinamically with more than 1 column. You just put all buttons together in a list and run:
```python
lines = array_chunk(buttons, 2)
keyboard = ikb(lines)
```
This will generate a list of lines with 2 buttons on each one.

### `pyromod.nav`
Tools for creating navigation keyboards.

- `pyromod.nav.Pagination`
Creates a full paginated keyboard. Usage:
```python
from pyrogram import Client, filters
from pyromod.nav import Pagination
from pyromod.helpers import ikb

def page_data(page):
    return f'view_page {page}'
def item_data(item, page):
    return f'view_item {item} {page}'
def item_title(item, page):
    return f'Item {item} of page {page}'

@Client.on_message(filters.regex('/nav'))
async def on_nav(c,m):
    objects = [*range(1,100)]
    page = Pagination(
        objects,
        page_data=page_data, # callback to define the callback_data for page buttons in the bottom
        item_data=item_data, # callback to define the callback_data for each item button
        item_title=item_title # callback to define the text for each item button
    )
    index = 0 # in which page is it now? (used to calculate the offset)
    lines = 5 # how many lines of the keyboard to include for the items
    columns = how many columns include in each items' line
    kb = page.create(index, lines, columns)
    await m.reply('Test', reply_markup=ikb(kb))
```

## pyromod.PyrogramConfig
It lets you do some tweaks on pyromod behavior.
```python
class PyromodConfig:
    timeout_handler = None
    stopped_handler = None
    throw_exceptions = True
    unallowed_click_alert = True
    unallowed_click_alert_text = (
        "[pyromod] You're not expected to click this button."
    )
```
`timeout_handler` and `stopped_handler` are callbacks that receive (identifier, listener_data) as arguments. timeout_handler receives an extra arg `timeout`. When they are in use, pyromod won't throw the exceptions ListenerStopped and ListenedTimeout.

### Copyright & License
This project may include snippets of Pyrogram code
- Pyrogram - Telegram MTProto API Client Library for Python. Copyright (C) 2017-2022 Dan <<https://github.com/delivrance>>

Licensed under the terms of the [GNU Lesser General Public License v3 or later (LGPLv3+)](COPYING.lesser)


