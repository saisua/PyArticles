from typing import *

from Lang.style.defaults import DEFAULT_CLEAR

def clear(
		  block: 'Block', 
		  clear: Union[
			  Literal['none'],
			  Literal['left'],
			  Literal['right'],
			  Literal['both'],
			  Literal['inherit'],
		  ]='both'
		) -> Self:
	clear_key, clear_value = DEFAULT_CLEAR
	
	block.style[clear_key] = clear_value.format(clear=clear)

	return block
	
