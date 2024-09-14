from Lang.html.base_tag import BaseTag, Block
from Lang.id import HEAD_ID

from Lang.compatibility import *

class head(BaseTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('head', *args, block_id=HEAD_ID, next_blocks=next_blocks, **kwargs)
