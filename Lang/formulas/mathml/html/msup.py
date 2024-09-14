from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import MSUP_ID

from Lang.compatibility import *

class msup(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('msup', *args, block_id=MSUP_ID, next_blocks=next_blocks, **kwargs)
