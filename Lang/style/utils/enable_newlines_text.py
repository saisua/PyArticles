from typing import *

from Lang.style.defaults import DEFAULT_NEWLINES

def enable_newlines_text(block: 'Block') -> Self:
	newlines_key, newlines_value = DEFAULT_NEWLINES
	
	block.style[newlines_key] = newlines_value

	return block
	