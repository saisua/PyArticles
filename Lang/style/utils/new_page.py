from typing import *

from Lang.style.defaults import DEFAULT_PAGE_BREAK

def new_page(block: 'Block') -> Self:
	new_page_key, new_page_value = DEFAULT_PAGE_BREAK
	
	block.style[new_page_key] = new_page_value
	return block
	