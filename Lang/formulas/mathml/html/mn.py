from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import MN_ID

from Lang.compatibility import *

class mn(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('mn', *args, block_id=MN_ID, next_blocks=next_blocks, **kwargs)
