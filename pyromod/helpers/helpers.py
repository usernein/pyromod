import asyncio
import json
import re

from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup

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

class LangsFormatMap(dict):
    def __missing__(self, key):
        return '{'+key+'}'

class LangString(str):
    def __call__(self, **kwargs):
        try:
            result = self
        except:
            result = key
            
        return result.format_map(LangsFormatMap(**kwargs))
        
class Langs:
    def __init__(self, strings=None, **kwargs):
        if not kwargs and not strings:
            raise ValueError('Pass the languages and the path to their JSON files as keyword arguments (language=path)')
        self.strings = strings or {}
        if not strings:
            for language_code,strings_file_path in kwargs.items():
                with open(strings_file_path) as fp:
                    self.strings[language_code] = json.load(fp)
                    self.strings[language_code].update({'language_code': language_code})
        
        #self.strings = {'en':{'start':'Hi {name}!'}}
        self.languages = list(self.strings.keys())
        self.language = 'en' if 'en' in self.languages else self.languages[0]
    
    def __getattr__(self, key):
        try:
            result = self.strings[self.language][key]
        except:
            result = key
        return LangString(result)
    
    def setLanguage(self, language_code):
        clean_lang_code = re.sub('[^a-z]', '', (language_code or '').lower())
        if not clean_lang_code:
            raise ValueError('Invalid language_code')
            
        lang_copy = Langs(strings=self.strings)
        if clean_lang_code in lang_copy.languages:
            lang_copy.language = clean_lang_code
        return lang_copy

def array_chunk(input, size):
    return [input[i : i + size] for i in range(0, len(input), size)]

def try_int(value):
    try:
        return int(value)
    except ValueError:
        return value

def color_json(JSON):
    if not isinstance(JSON, str):
        JSON = json.dumps(JSON, ensure_ascii=False, indent=2)
    JSON = re.sub('(?<=[\[:]) ?(\d+)', YELLOW+r'\1'+RESET, JSON)
    JSON = re.sub(r'("(?:[^"\\]|\\.)*")', GREEN+r'\1'+RESET, JSON)
    JSON = re.sub('false', RED+'false'+RESET, JSON)
    JSON = re.sub('true', BLUE+'true'+RESET, JSON)
    print(JSON)
    
def switch_case(switch, cases):
    if switch in cases:
        return cases[switch]
    elif 'default_case' in cases:
        return cases['default_case']
    else:
        return None