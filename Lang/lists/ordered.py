from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.text.text import _text as text
from Lang.id import ORDERED_LIST_ID, ORDERED_LIST_ITEM_ID

class _ordered_list_item(TextTag):
	def __init__(self, next_blocks: str | Block | List[Block], *args, **kwargs) -> None:
		if(isinstance(next_blocks, str)):
			next_blocks = text(next_blocks)
		
		super().__init__('li', *args, block_id=ORDERED_LIST_ITEM_ID, next_blocks=next_blocks, **kwargs)


class ordered_list(TextTag):
	def __init__(self, items: List[str | Block | List[Block]], *args, **kwargs) -> None:
		super().__init__(
			'ol', 
			*args, 
			block_id=ORDERED_LIST_ID, 
			next_blocks=list(map(
				_ordered_list_item, 
				items
			)), 
			**kwargs
		)