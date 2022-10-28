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

def dice(ctx, message):
    return hasattr(message, 'dice') and message.dice
pyrogram.filters.dice = dice

async def group_admin(_, client: pyrogram.Client, m: pyrogram.types.Message):
    if (
        m.chat.type != pyrogram.enums.ChatType.SUPERGROUP
        and m.chat.type != pyrogram.enums.ChatType.GROUP
    ):
        return False
    id = m.from_user.id
    admins = []
    async for m in client.get_chat_members(m.chat.id, filter=pyrogram.enums.ChatMembersFilter.ADMINISTRATORS):
        admins.append(m.user.id)
    return id in admins


pyrogram.filters.group_admin = pyrogram.filters.create(group_admin)