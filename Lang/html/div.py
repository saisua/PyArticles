from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import DIV_ID

class div(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('div', *args, block_id=DIV_ID, next_blocks=next_blocks, **kwargs)