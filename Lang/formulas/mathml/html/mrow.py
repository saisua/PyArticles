from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import MROW_ID

class mrow(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('mrow', *args, block_id=MROW_ID, next_blocks=next_blocks, **kwargs)
