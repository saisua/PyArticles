from typing import *

from Lang.core.block import Block
from Lang.html.base_tag import BaseTag
from Lang.id import HORIZONTAL_DIVIDER_ID

class horizontal_divider(BaseTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('hr', *args, block_id=HORIZONTAL_DIVIDER_ID, next_blocks=next_blocks, **kwargs)