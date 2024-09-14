from Lang.style.defaults import DEFAULT_FONT_SIZE

from Lang.compatibility import *

def font_size(
		block: Optional['Block'],
		size: Union[
			Literal['xx-small'],
			Literal['x-small'],
			Literal['small'],
			Literal['medium'],
			Literal['large'],
			Literal['x-large'],
			Literal['xx-large'],
			Literal['xxx-large'],
			Literal['smaller'],
			Literal['larger'],
			Literal['math'],
			Literal['inherit'],
			Literal['initial'],
			Literal['revert'],
			Literal['revert-layer'],
			Literal['unset'],
			Annotated[str, "In pixels: '12px'"],
			Annotated[str, "In em: '12em'"],
			Annotated[str, "In percentage: '12%'"],
		]
	):
	if(block is None):
		return

	font_size_key, font_size_value = DEFAULT_FONT_SIZE

	block.style[font_size_key] = font_size_value.format(size=size)
	return block
