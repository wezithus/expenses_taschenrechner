# -*- coding: utf-8 -*-
# aufzeichnungen/datasets.py

""" this module provides constant/non contant datasets """

from .helpers import ReadonlyDict

DIGIT_TYPES = ReadonlyDict({ 1 : 2, 2 : 3 })

CURFEWS = ReadonlyDict({ 0 : "FirstHalf", 1 : "SecondHalf"})

CURFEWS_LABEL = ReadonlyDict({
    2 : {
        "FirstHalf" : "နေ့လည်",
        "SecondHalf" : "ညနေ",
    },
    3 : {
        "FirstHalf" : "၁ - ၁၆",
        "SecondHalf" : "၁၆ - ၃၀",
    }
})
