"""
pyromod - A monkeypatcher add-on for Pyrogram
Copyright (C) 2020 Cezar H. <https://github.com/usernein>

This file is part of pyromod.

pyromod is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyromod is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyromod.  If not, see <https://www.gnu.org/licenses/>.
"""

import pyrogram 
import re

from ..utils import patch, patchable

# To allow Filters.callback_regex to exist:
pyrogram.client.types.bots_and_keyboards.callback_query.CallbackQuery.matches = None 

@patch(pyrogram.client.filters.filters.Filters)
class Filters:
    create = pyrogram.client.filters.filters.Filters.create
    
    @patchable
    @create
    @staticmethod
    def dice(ctx, message):
        return hasattr(message, 'dice') and message.dice
    
    @patchable
    @create
    @staticmethod
    def callback_regex(pattern, flags: int = 0):
        def callback_regex_filter(ctx, query):
            if query.data:
                query.matches = [*ctx.pattern.finditer(query.data)] or None
            return bool(query.matches)
        return Filters.create(callback_regex_filter, pattern=re.compile(pattern, flags))
