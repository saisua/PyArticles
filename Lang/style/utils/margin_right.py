from typing import *

from Lang.style.defaults import DEFAULT_APPLY_TO_TEXT_WITH_NEWLINES, DEFAULT_MARGIN_RIGHT

def margin_right(block: 'Block', margin: str) -> Self:
	margin_right_key, margin_right_value = DEFAULT_MARGIN_RIGHT
	
	block.style[margin_right_key] = margin_right_value.format(margin=margin)

	text_with_newlines_key, text_with_newlines_value = DEFAULT_APPLY_TO_TEXT_WITH_NEWLINES

	block.style[text_with_newlines_key] = text_with_newlines_value

	return block
	