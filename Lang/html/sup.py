from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import SUP_ID

class sup(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		style = kwargs.get('style', dict())

		# TODO: Change to Final strings
		if('vertical-align' not in style):
			style['vertical-align'] = 'super'
		if('font-size' not in style):
			style['font-size'] = 'smaller'

		kwargs['style'] = style

		super().__init__('sup', *args, block_id=SUP_ID, next_blocks=next_blocks, **kwargs)
