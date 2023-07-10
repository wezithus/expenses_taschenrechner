# -*- coding: utf-8 -*-
# aufzeichnungen/helpers.py

""" this module provides helper methods """

""" validation """
""" validation ends """

"""datasets"""
from typing import Any


class ReadonlyDict(dict):
    __read_only__ = True

    def __setitem__(self, __key: Any, __value: Any) -> None:
        if self.__read_only__:
            raise TypeError("Can't modify readonly dict")
        return super().__setitem__(__key, __value)
"""end datasets"""
