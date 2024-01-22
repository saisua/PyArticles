from typing import *

from Lang.style.defaults import DEFAULT_ALIGN_TEXT

def align_text(
		block: 'Block', 
		alignment: Union[
			Literal['left'],
			Literal['right'],
			Literal['center'],
			Literal['justify'],
			Literal['justify-all'],
			Literal['start'],
			Literal['end'],
			Literal['match-parent'],
			Literal['-moz-center'],
			Literal['-webkit-center'],
			Literal['inherit'],
			Literal['initial'],
			Literal['unset'],
		]) -> Self:
	alignment_key, alignment_value = DEFAULT_ALIGN_TEXT
	
	block.style[alignment_key] = alignment_value.format(alignment=alignment)

	return block
	