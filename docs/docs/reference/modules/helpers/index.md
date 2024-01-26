---
title: pyromod.helpers
---

### *function* `pyromod.array_chunk(input_array, size)`

Split an array into chunks.

#### Parameters

| Parameter   | Type   | Description             |
|-------------|--------|-------------------------|
| input_array | `list` | The array to split.     |
| size        | `int`  | The size of each chunk. |

#### Return

A list of chunks.

### *function* `pyromod.bki(keyboard)`

Deserialize an InlineKeyboardMarkup to a list of lists of buttons.

#### Parameters

| Parameter | Type                     | Description                 |
|-----------|--------------------------|-----------------------------|
| keyboard  | `InlineKeyboardMarkup`   | An InlineKeyboardMarkup.    |

#### Return

A list of lists of buttons.

### *function* `pyromod.btn(text, value, type='callback_data')`

Create an InlineKeyboardButton.

#### Parameters

| Parameter | Type   | Description                 |
|-----------|--------|-----------------------------|
| text      | `str`  | The text of the button.     |
| value     | `str`  | The value of the button.    |
| type      | `str`  | The type of the button.     |

#### Return

An InlineKeyboardButton.

### *function* `pyromod.force_reply(selective=True)`

Create a ForceReply.

#### Parameters

| Parameter | Type    | Description                                                                 |
|-----------|---------|-----------------------------------------------------------------------------|
| selective | `bool`  | Whether the reply should be selective.                                      |

#### Return

A ForceReply.

### *function* `pyromod.ikb(rows=None)`

Create an InlineKeyboardMarkup from a list of lists of buttons.

#### Parameters

| Parameter | Type                               | Description                 |
|-----------|------------------------------------|-----------------------------|
| rows      | `list[list[InlineKeyboardButton]]` | A list of lists of buttons. |

#### Return

An InlineKeyboardMarkup.

### *function* `pyromod.kb(rows=None, **kwargs)`

Create a ReplyKeyboardMarkup from a list of lists of buttons.

#### Parameters

| Parameter  | Type                         | Description                                       |
|------------|------------------------------|---------------------------------------------------|
| rows       | `list[list[KeyboardButton]]` | A list of lists of buttons.                       |
| \*\*kwargs | `dict`                       | Keyword arguments to pass to ReplyKeyboardMarkup. |

#### Return

A ReplyKeyboardMarkup.

### *function* `pyromod.kbtn`

alias of `KeyboardButton`

### *function* `pyromod.ntb(button)`

Deserialize an InlineKeyboardButton to btn() format.

#### Parameters

| Parameter | Type                     | Description                 |
|-----------|--------------------------|-----------------------------|
| button    | `InlineKeyboardButton`   | An InlineKeyboardButton.    |

#### Return

A btn() format button.
