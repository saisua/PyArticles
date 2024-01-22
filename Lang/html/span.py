from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import SPAN_ID

class span(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('span', *args, block_id=SPAN_ID, next_blocks=next_blocks, **kwargs)