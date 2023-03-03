from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ForceReply,
)

button_types = ["callback_data", "url", "switch_inline_query", "switch_inline_query_current_chat", "callback_game"]


def ikb(rows=list[tuple | str | dict] | list[list[tuple | str | dict]],
        column: int = 0,
        Markup: bool = True) -> InlineKeyboardMarkup | list[list[InlineKeyboardButton]]:
    """Creates inline keyboard.

    :param rows: Items that should turn to InlineKeyboard. **NOTE**: If you want your buttons have specific position as
        you defined, you should pass like list[list[buttons], list[buttons]].

    :param column: Pass the number of columns that you want. **MAX** is 6.

    :param Markup: If False, returned lists won't be InlineKeyboardMarkup.
    """

    lines = []
    line = []
    split = False if isinstance(rows[0], list) and column == 0 else True

    for row in rows:
        if isinstance(row, list):
            for button in row:
                line.append(btn(button))

            if not split:
                lines.append(line.copy())
                line.clear()

        else:
            line.append(btn(row)) if split else lines.append([btn(row)])

    if split:
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


def kb(rows: list[str | dict] | list[list[str | dict]], column: int = 2, **kwargs) -> ReplyKeyboardMarkup:
    """Creates Keyboard Button.

    :param rows: Items that should turn to KeyboardButton. **NOTE**: If you want your buttons have specific position as
        you defined, you should pass like list[list[buttons], list[buttons]].

    :param column: Pass the number of columns that you want. **MAX** is 4.

    :param kwargs: set ReplyKeyboardMarkup Args, is_persistent, resize_keyboard, one_time_keyboard, selective,
        placeholder
    """

    lines = []
    line = []
    split = False if isinstance(rows[0], list) else True

    for row in rows:
        if isinstance(row, list):
            for button in row:
                line.append(_kbtn(button))

            if not split:
                lines.append(line.copy())
                line.clear()

        else:
            line.append(_kbtn(row)) if split else lines.append(_kbtn(row))

    if split:
        column = column if 1 <= column <= 4 else 4
        lines.extend(
            Split(line, column)
        )

    return ReplyKeyboardMarkup(keyboard=lines, **kwargs)


def _kbtn(button: str | dict) -> KeyboardButton:
    return KeyboardButton(**button) if isinstance(button, dict) else KeyboardButton(button)


kbtn = KeyboardButton


def force_reply(selective=True):
    return ForceReply(selective=selective)


def Split(List: list, column: int) -> None:
    return [List[i:i + column] for i in range(0, len(List), column)]
