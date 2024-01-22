from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.text.text import _text as text
from Lang.id import UNORDERED_LIST_ID, UNORDERED_LIST_ITEM_ID

class _unordered_list_item(TextTag):
	def __init__(self, next_blocks: str | Block | List[Block], *args, **kwargs) -> None:
		if(isinstance(next_blocks, str)):
			next_blocks = text(next_blocks)
		
		super().__init__('li', *args, block_id=UNORDERED_LIST_ITEM_ID, next_blocks=next_blocks, **kwargs)


class unordered_list(TextTag):
	def __init__(self, items: List[str | Block | List[Block]], *args, **kwargs) -> None:
		super().__init__(
			'ul', 
			*args, 
			block_id=UNORDERED_LIST_ID, 
			next_blocks=list(map(
				_unordered_list_item, 
				items
			)), 
			**kwargs
		)