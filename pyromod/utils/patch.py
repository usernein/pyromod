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
from contextlib import contextmanager, asynccontextmanager
from inspect import iscoroutinefunction
from typing import Callable, T, Type

from pyrogram.sync import async_to_sync


def patch_into(target_class):
    def is_patchable(item):
        func = item[1]
        return getattr(func, "should_patch", False)

    def wrapper(container: Type[T]) -> T:
        for name, func in filter(is_patchable, container.__dict__.items()):
            old = getattr(target_class, name, None)
            if old is not None:  # Not adding 'old' to new func
                setattr(target_class, "old" + name, old)

            # Worse Code
            tempConf = {
                i: getattr(func, i, False)
                for i in ["is_property", "is_static", "is_context"]
            }

            async_to_sync(container, name)
            func = getattr(container, name)

            for tKey, tValue in tempConf.items():
                setattr(func, tKey, tValue)

            if func.is_property:
                func = property(func)
            elif func.is_static:
                func = staticmethod(func)
            elif func.is_context:
                if iscoroutinefunction(func.__call__):
                    func = asynccontextmanager(func)
                else:
                    func = contextmanager(func)

            setattr(target_class, name, func)
        return container

    return wrapper


def should_patch(
    is_property: bool = False, is_static: bool = False, is_context: bool = False
) -> Callable:
    """
    A decorator that marks a function as patchable.

    Usage:

        @patchable(is_property=True)
        def my_property():
            ...

        @patchable(is_static=True)
        def my_static_method():
            ...

        @patchable(is_context=True)
        def my_context_manager():
            ...

        @patchable(is_property=False, is_static=False, is_context=False)
        def my_function():
            ...

        @patchable()
        def default_usage():
            ...

    Parameters:
        - is_property (bool): whether the function is a property. Default is False.
        - is_static (bool): whether the function is a static method. Default is False.
        - is_context (bool): whether the function is a context manager. Default is False.

    Returns:
        - A callable object that marks the function as patchable.
    """

    def wrapper(func: Callable) -> Callable:
        func.should_patch = True
        func.is_property = is_property
        func.is_static = is_static
        func.is_context = is_context
        return func

    return wrapper
