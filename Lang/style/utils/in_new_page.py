from typing import *

from Lang.style.defaults import DEFAULT_IN_NEW_PAGE

def in_new_page(block: Optional['Block']) -> Self:
	if(block is None):
		return
	
	in_new_page_key, in_new_page_value = DEFAULT_IN_NEW_PAGE
	
	block.style[in_new_page_key] = in_new_page_value
	return block
	