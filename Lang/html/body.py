from typing import *

from Lang.html.base_tag import BaseTag, Block
from Lang.id import BODY_ID

class body(BaseTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('body', *args, block_id=BODY_ID, next_blocks=next_blocks, **kwargs)