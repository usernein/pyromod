---
title: Identifier
---

## *class* pyromod.types.Identifier

The `pyromod.types.Identifier` class is a dataclass that serves as a utility for matching listeners to the data of updates.

### *Constructor parameters*

Parameter | Type | Description
--- | --- | ---
`inline_message_id` | `str` | The inline message ID to match. If `None`, it is not considered for matching.
`chat_id` | `int` | The chat ID to match. If `None`, it is not considered for matching.
`message_id` | `int` | The message ID to match. If `None`, it is not considered for matching.
`from_user_id` | `int` | The user ID to match. If `None`, it is not considered for matching.

### *method* `matches`

> *method* `matches(other: Identifier) -> bool`

Compares the `Identifier` with another `Identifier` instance to determine if they match.

#### Parameters:

Parameter | Type | Description
--- | --- | ---
`other` | `pyromod.types.Identifier` | The `Identifier` to compare against.

#### Returns:
`True` if the two `Identifier` instances match, meaning that for each property in `other`,
either the property in the current `Identifier` (self) is `None` (i.e. allowing `other` to have any value) or it has the
same value. `False` otherwise.

### *method* `count_populated`

> *method* `count_populated() -> int`

Counts the number of non-null properties in the `Identifier`.

#### Returns:

An integer representing the count of non-null properties in the `Identifier`.
