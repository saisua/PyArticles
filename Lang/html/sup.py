from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import SUP_ID

from Lang.style.defaults import DEFAULT_VERTICAL_ALIGN, DEFAULT_FONT_SIZE

from Lang.compatibility import *

class sup(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		style = kwargs.get('style', dict())

		alignment_key, alignment_value = DEFAULT_VERTICAL_ALIGN
		if(alignment_key not in style):
			style[alignment_key] = alignment_value.format(alignment="super")

		font_size_key, font_size_value = DEFAULT_FONT_SIZE
		if(font_size_key not in style):
			style[font_size_key] = font_size_value.format(size='smaller')

		kwargs['style'] = style

		super().__init__('sup', *args, block_id=SUP_ID, next_blocks=next_blocks, **kwargs)
