from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import MATH_ID

from Lang.compatibility import *

class math(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('math', *args, block_id=MATH_ID, next_blocks=next_blocks, **kwargs)
