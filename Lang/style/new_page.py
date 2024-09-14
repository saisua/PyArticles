from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.id import NEW_PAGE_ID

from Lang.compatibility import *

class new_page(TextTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		kwargs['class'] = 'new_page'
		super().__init__('div', *args, block_id=NEW_PAGE_ID, next_blocks=next_blocks, **kwargs)

	def __repr__(self) -> str:
		return "<new_page>"