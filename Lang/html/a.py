from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import A_ID

class a(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('a', *args, block_id=A_ID, next_blocks=next_blocks, **kwargs)