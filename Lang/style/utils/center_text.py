from typing import *

from Lang.style.defaults import DEFAULT_ALIGN_TEXT_CENTER

def center_text(block: 'Block') -> Self:
	center_key, center_value = DEFAULT_ALIGN_TEXT_CENTER
	
	block.style[center_key] = center_value

	return block
	