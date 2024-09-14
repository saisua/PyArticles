from Lang.style.defaults import DEFAULT_APPLY_TO_TEXT_WITH_NEWLINES, DEFAULT_MARGIN_LEFT

from Lang.compatibility import *

def margin_left(block: 'Block', margin: str) -> Self:
	margin_left_key, margin_left_value = DEFAULT_MARGIN_LEFT
	
	block.style[margin_left_key] = margin_left_value.format(margin=margin)

	text_with_newlines_key, text_with_newlines_value = DEFAULT_APPLY_TO_TEXT_WITH_NEWLINES

	block.style[text_with_newlines_key] = text_with_newlines_value

	return block
	
