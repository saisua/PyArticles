from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import MTEXT_ID

class mtext(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('mtext', *args, block_id=MTEXT_ID, next_blocks=next_blocks, **kwargs)