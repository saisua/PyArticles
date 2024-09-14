from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import BR_ID

from Lang.compatibility import *

class br(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('br', *args, block_id=BR_ID, next_blocks=next_blocks, **kwargs)
