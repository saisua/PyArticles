from Lang.style.defaults import DEFAULT_DONT_SPLIT

from Lang.compatibility import *

def dont_split(block: 'Block') -> Self:
	dont_split_key, dont_split_value = DEFAULT_DONT_SPLIT
	
	block.style[dont_split_key] = dont_split_value
	return block
	
