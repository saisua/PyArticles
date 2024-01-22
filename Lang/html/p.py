from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import P_ID

class p(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('p', *args, block_id=P_ID, next_blocks=next_blocks, **kwargs)