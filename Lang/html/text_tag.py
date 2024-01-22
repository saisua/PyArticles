from typing import *

from Lang.html.base_tag import BaseTag

from Lang.style.utils.center_text import center_text
from Lang.style.utils.align_text import align_text
from Lang.style.utils.line_through import line_through
from Lang.style.utils.vertical_align import vertical_align

class TextTag(BaseTag):
	center = center_text
	align = align_text
	line_through = line_through
	vertical_align = vertical_align