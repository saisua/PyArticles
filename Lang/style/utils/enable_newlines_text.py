from Lang.style.defaults import DEFAULT_NEWLINES

from Lang.compatibility import *

def enable_newlines_text(block: 'Block') -> Self:
	newlines_key, newlines_value = DEFAULT_NEWLINES
	
	block.style[newlines_key] = newlines_value

	return block
	
