from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

def ikb(rows = []):
    lines = []
    for row in rows:
        line = []
        for button in row:
            button = btn(*button) # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    return InlineKeyboardMarkup(inline_keyboard=lines)
    #return {'inline_keyboard': lines}

def btn(text, value, type = 'callback_data'):
    return InlineKeyboardButton(text, **{type: value})
    #return {'text': text, type: value}

def kb(rows = [], **kwargs):
    lines = []
    for row in rows:
        line = []
        for button in row:
            button_type = type(button)
            if button_type == str:
                button = KeyboardButton(button)
            elif button_type == dict:
                button = KeyboardButton(**button)
            
            line.append(button)
        lines.append(line)
    return ReplyKeyboardMarkup(keyboard=lines, **kwargs)

kbtn = KeyboardButton

def array_chunk(input, size):
    return [input[i:i+size] for i in range(0, len(input), size)]

