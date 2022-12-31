# pyromod
A monkeypatcher add-on for Pyrogram which does conversation handling and other cool stuff

In other words, it is a compilation of utils i developed for extending my personal use of Pyrogram.
It works **together** with pyrogram, this is **not** a fork/ modded version. It does monkeypatching to add features to Pyrogram classes (so i don't need to update on every Pyrogram's release).

## Usage'   
Import `pyromod` one time in your script and you'll be able to use the modified pyrogram in all the scripts running in the same proccess. Example:
```python
import pyromod
from pyrogram import Client

app = Client('my_session')
```

Then you can, from another file, do `from your_script.py import app` to import the modded Pyrogram Client we created above. It will be modded globally.

All the patches are applied automatically as soon as pyromod is imported. And there is the module `pyromod.helpers`, which provides classes and functions that should be explicitely imported in order to be used.

## Methods
All pyromod methods are callable by any of these ways:
- `await Client.<method>(chat_id...)`
- `await Chat.<method>()`
- `await User.<method>()`

In the last two, Pyrogram automatically gets the id of the object.
These are the methods pyromod adds:
- `listen(chat_id=None, filters=None, timeout=30)`
Awaits for a new message in the specified chat and returns it
You can pass Update Filters to the `filters` parameter just like you do for the update handlers. e.g. `filters=filters.photo & filters.bot`

- `ask(text, chat_id=None, filters=None, timeout=30)`
Same as `listen`, but sends a message before and only then waits for a response.
You can additionally pass any of the `Client.send_message()` parameters. Check the example below.
The object of the sent message is returned inside of the attribute `request`

Example:
```python
import pyromod
from pyrogram import Client
client = Client(...)
...
    answer = await client.ask(chat_id, '*Send me your name:*', parse_mode=enums.ParseMode.MARKDOWN)
    await answer.request.edit_text("Name received!")
    await answer.reply(f'Your name is: {answer.text}', quote=True)    
```

## `pyromod.helpers`
Tools for creating inline keyboards a lot easier.

### `pyromod.helpers.ikb`

Creates a inline keyboard.
Its first and only argument is a list (the keyboard itself) containing lists (the lines) of buttons, which can be lists or tuples. I use tuples to avoid a mess with a lot of brackets. Tuples makes it easier to read.

The button syntax is very simple: `(TEXT, VALUE, TYPE)`, with TYPE being any existent button type (e.g. `url`) and VALUE is its value. If you omit the type, it will be considered as a callback button.
This syntax will be automagically converted by pyromod.

Examples:
```python
from pyromod.helpers import ikb
...
keyboard = ikb([
    [('Button 1', 'call_1'), ('Button 2', 'call_2')],
    [('Another button', 't.me/pyromodchat', 'url')]
])
await message.reply('Easiest inlike keyboard', reply_markup=keyboard)
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

### Copyright & License
This project may include snippets of Pyrogram code
- Pyrogram - Telegram MTProto API Client Library for Python. Copyright (C) 2017-2022 Dan <<https://github.com/delivrance>>

Licensed under the terms of the [GNU Lesser General Public License v3 or later (LGPLv3+)](COPYING.lesser)

