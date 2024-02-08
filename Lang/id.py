from typing import *
from enum import IntEnum

class IDs(IntEnum):
	HTML_ID: Final[int] = 1
	HEAD_ID: Final[int] = 2
	BODY_ID: Final[int] = 3
	LINK_STYLESHEET_ID: Final[int] = 4
	TITLE_ID: Final[int] = 5
	TEXT_ID: Final[int] = 6
	H_ID: Final[int] = 7
	A_ID: Final[int] = 8
	P_ID: Final[int] = 9
	ORDERED_LIST_ID: Final[int] = 10
	ORDERED_LIST_ITEM_ID: Final[int] = 11
	UNORDERED_LIST_ID: Final[int] = 12
	UNORDERED_LIST_ITEM_ID: Final[int] = 13
	NAMED_LIST_ID: Final[int] = 14
	NAMED_LIST_KEY_ID: Final[int] = 15
	NAMED_LIST_VALUE_ID: Final[int] = 16
	IMG_ID: Final[int] = 17
	SECTION_ID: Final[int] = 18
	DIV_ID: Final[int] = 19
	TD_ID: Final[int] = 20
	TR_ID: Final[int] = 21
	TBODY_ID: Final[int] = 22
	TABLE_ID: Final[int] = 23
	TH_ID: Final[int] = 24
	SPAN_ID: Final[int] = 25
	B_ID: Final[int] = 26
	HORIZONTAL_DIVIDER_ID: Final[int] = 27
	VERTICAL_DIVIDER_ID: Final[int] = 28
	MFRAC_ID: Final[int] = 28
	MN_ID: Final[int] = 29
	MATH_ID: Final[int] = 30
	MI_ID: Final[int] = 31
	MO_ID: Final[int] = 32
	MTEXT_ID: Final[int] = 33
	LINK_SCRIPT_ID: Final[int] = 34
	NEW_PAGE_ID: Final[int] = 35
	ACRONYM_ID: Final[int] = 36
	FIGURE_ID: Final[int] = 37
	FIGCAPTION_ID: Final[int] = 38
	BR_ID: Final[int] = 39

globals().update(dict(filter(lambda x: not x[0].startswith('_'), IDs.__dict__.items())))
