### *class* pyromod.types.Identifier

The `pyromod.types.Identifier` class is a dataclass that serves as a utility for matching listeners to the data of updates.

### *Parameters:*

- **inline_message_id** (*str or None*) – The inline message ID to match. If `None`, it is not considered for matching.
- **chat_id** (*int or None*) – The chat ID to match. If `None`, it is not considered for matching.
- **message_id** (*int or None*) – The message ID to match. If `None`, it is not considered for matching.
- **from_user_id** (*int or None*) – The user ID to match. If `None`, it is not considered for matching.

### *matches(other: Identifier) -> bool*

Compares the `Identifier` with another `Identifier` instance to determine if they match.

**Parameters:**

- **other** (*pyromod.types.Identifier*) – The `Identifier` to compare against.

**Returns:**
`True` if the two `Identifier` instances match, meaning that for each property in `other`,
either the property in the current `Identifier` (self) is `None` (i.e. allowing `other` to have any value) or it has the
same value. `False` otherwise.

### *count_populated() -> int*

Counts the number of non-null properties in the `Identifier`.

**Returns:**
An integer representing the count of non-null properties in the `Identifier`.
