from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ForceReply,
)


button_types = ["callback_data", "url", "switch_inline_query", "switch_inline_query_current_chat", "callback_game"]


def ikb(rows=list[tuple | str | dict] | list[list[tuple | str | dict]],
        column: int | str = 1,
        Markup: bool = True) -> InlineKeyboardMarkup | list[list[InlineKeyboardButton]]:
    """Creates inline keyboard.

    :param rows: Items that should turn to InlineKeyboard.

    :param column: Pass the number of columns that you want **MAX** is 6. **NOTE**: If you want keep your list position
        that you've defined, you **should** pass string. it can be empty "" or whatever you want like "keep".

    :param Markup: If False, returned lists won't be InlineKeyboardMarkup.
    """

    lines = []
    line = []
    for row in rows:
        if isinstance(row, list):
            for button in row:
                line.append(btn(button))

            if isinstance(column, str):
                lines.append(line.copy())
                line.clear()
        else:
            line.append(btn(row))

    if isinstance(column, int):
        column = column if 1 <= column <= 6 else 6
        lines.extend(
            Split(line, column)
        )

    return mark_ikb(lines) if Markup else lines


def btn(button: tuple | str | dict) -> InlineKeyboardButton:
    if isinstance(button, tuple):
        if len(button) == 3:
            text, value, Type = button
        else:
            text, value, Type = (button[0], *button) if button[1] in button_types else (*button, "callback_data")

        button = InlineKeyboardButton(text, **{Type: value})

    elif isinstance(button, str):
        button = InlineKeyboardButton(button, **{"callback_data": button})

    else:
        button = InlineKeyboardButton(**button)

    return button


def mark_ikb(List) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=List)


# The inverse of ikb
def bki(keyboard) -> list[list[tuple[str, str] | str]]:
    lines = []
    for row in keyboard.inline_keyboard:
        line = []
        for button in row:
            button = ntb(button)  # btn() format
            line.append(button)

        lines.append(line.copy())
        line.clear()
    return lines
    # return ikb() format


def ntb(button) -> tuple[str, str] | str:
    for btn_type in button_types:
        value = getattr(button, btn_type)
        if value:
            break

    button = (button.text, value) if button.text != value else button.text
    if btn_type != "callback_data":
        button = (button, btn_type)
    return button


def kb(rows: list[str | dict] | list[list[str | dict]], column: int | str = 2, **kwargs) -> ReplyKeyboardMarkup:
    """Creates Keyboard Button.

    :param rows: Items that should turn to KeyboardButton.

    :param column: Pass the number of columns that you want **MAX** is 4. **NOTE**: If you want keep your list position
        that you've defined, you **should** pass string. it can be empty "" or whatever you want like "keep".
    """

    lines = []
    line = []

    for row in rows:
        if isinstance(row, list):
            for button in row:
                line.append(
                    KeyboardButton(**button) if isinstance(button, dict) else KeyboardButton(button)
                )

            if isinstance(column, str):
                lines.append(line.copy())
                line.clear()
        else:
            line.append(
                KeyboardButton(**row) if isinstance(row, dict) else KeyboardButton(row)
            )

    if isinstance(column, int):
        column = column if 1 <= column <= 4 else 4
        lines.extend(
            Split(line, column)
        )

    return ReplyKeyboardMarkup(keyboard=lines, **kwargs)


kbtn = KeyboardButton


def force_reply(selective=True):
    return ForceReply(selective=selective)


def Split(List: list, column: int) -> None:
    return [List[i:i + column] for i in range(0, len(List), column)]
