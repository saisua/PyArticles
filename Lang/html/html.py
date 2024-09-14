from Lang.html.base_tag import BaseTag, Block
from Lang.id import HTML_ID

from Lang.compatibility import *

class html(BaseTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('html', *args, block_id=HTML_ID, next_blocks=next_blocks, **kwargs)
