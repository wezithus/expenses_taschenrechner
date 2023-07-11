# -*- coding: utf-8 -*-
# aufzeichnungen/helpers.py

""" this module provides helper methods """

""" validation """
""" validation ends """

"""helper classes"""
from typing import Any

MM_NUMBERS = ["၀", "၁", "၂", "၃", "၄", "၅", "၆", "၇", "၈", "၉"]

class BurInt():
    def __init__(self, value) -> None:
        match value:
            case str() if value.isnumeric():
                pass
            case int():
                value = str(value)
            case _:
                raise ValueError("Please provide an int or numeric input")
        self.value = value
        self._getBurmeseNumber()

    def _getBurmeseNumber(self):
        self.burmese_value =  "".join([MM_NUMBERS[int(i)] for i in self.value])
    
    def formatBurmeseValue(self):
        b, a = divmod(len(self.burmese_value), 3)
        return ",".join(([self.burmese_value[:a]] if a else []) + [self.burmese_value[a + 3 * i : a + 3 * i + 3] for i in range(b)])

class ReadonlyDict(dict):
    __read_only__ = True

    def __setitem__(self, __key: Any, __value: Any) -> None:
        if self.__read_only__:
            raise TypeError("Can't modify readonly dict")
        return super().__setitem__(__key, __value)
"""end datasets"""
