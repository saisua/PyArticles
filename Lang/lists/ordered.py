from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.text.text import _text as text
from Lang.id import ORDERED_LIST_ID, ORDERED_LIST_ITEM_ID

from Lang.compatibility import *

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

	def __repr__(self) -> str:
		"""
		Shows information about the useful attributes of the object when printed
		Any attribute with length is only shown when length > 0
		The id is not shown
		For the class attributes of type string, keep up to 15 characters max, and if the string is longer than that, add an ellipsis
		"""
		return "<OrderedList>"