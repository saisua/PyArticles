from Lang.html.base_tag import BaseTag, Block
from Lang.id import FIGCAPTION_ID

from Lang.compatibility import *

class figcaption(BaseTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('figcaption', *args, block_id=FIGCAPTION_ID, next_blocks=next_blocks, **kwargs)
