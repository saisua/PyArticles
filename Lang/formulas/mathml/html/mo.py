from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import MO_ID

class mo(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('mo', *args, block_id=MO_ID, next_blocks=next_blocks, **kwargs)