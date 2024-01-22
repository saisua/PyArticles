from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import MFRAC_ID

class mfrac(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('mfrac', *args, block_id=MFRAC_ID, next_blocks=next_blocks, **kwargs)