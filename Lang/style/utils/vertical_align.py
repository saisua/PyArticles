from typing import *

from Lang.style.defaults import DEFAULT_VERTICAL_ALIGN

def vertical_align(
		block: Optional['Block'], 
		alignment: Union[
			Literal['baseline'],
			Literal['sub'],
			Literal['super'],
			Literal['text-top'],
			Literal['text-bottom'],
			Literal['middle'],
			Literal['top'],
			Literal['bottom'],
			Literal['inherit'],
			Literal['initial'],
			Literal['revert'],
			Literal['revert-layer'],
			Literal['unset'],
			str
		]
	):
	if(block is None):
		return

	vertical_align_key, vertical_align_value = DEFAULT_VERTICAL_ALIGN
	
	block.style[vertical_align_key] = vertical_align_value.format(alignment=alignment)
	return block
	