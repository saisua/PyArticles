from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import TT_ID

from Lang.compatibility import *

class tt(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('tt', *args, block_id=TT_ID, next_blocks=next_blocks, **kwargs)
