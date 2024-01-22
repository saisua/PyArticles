from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import H_ID

class h(TextTag):
	def __init__(self, n: int, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__(f'h{n}', *args, block_id=H_ID, next_blocks=next_blocks, **kwargs)