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
from typing import Type, T


def patch(target_class):
    def is_patchable(item):
        func = item[1]
        return getattr(func, "patchable", False)

    def wrapper(base_class: Type[T]) -> T:
        for name, func in filter(is_patchable, base_class.__dict__.items()):
            old_value = getattr(target_class, name, None)

            setattr(target_class, "old" + name, old_value)
            setattr(target_class, name, func)
            
        return base_class

    return wrapper


def patchable(func: Type[T]) -> T:
    func.patchable = True
    return func
