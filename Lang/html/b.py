from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import B_ID

from Lang.compatibility import *

class b(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('b', *args, block_id=B_ID, next_blocks=next_blocks, **kwargs)
