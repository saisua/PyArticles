from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import MI_ID

from Lang.compatibility import *

class mi(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('mi', *args, block_id=MI_ID, next_blocks=next_blocks, **kwargs)
