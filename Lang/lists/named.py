from itertools import chain

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.text.text import _text as text
from Lang.id import NAMED_LIST_ID, NAMED_LIST_KEY_ID, NAMED_LIST_VALUE_ID

from Lang.compatibility import *

class _ordered_list_key(TextTag):
	def __init__(self, next_blocks: str | Block | List[Block], *args, **kwargs) -> None:
		if(isinstance(next_blocks, str)):
			next_blocks = text(next_blocks)
		
		super().__init__('dt', *args, block_id=NAMED_LIST_KEY_ID, next_blocks=next_blocks, **kwargs)

class _ordered_list_value(TextTag):
	def __init__(self, next_blocks: str | Block | List[Block], *args, **kwargs) -> None:
		if(isinstance(next_blocks, str)):
			next_blocks = text(next_blocks)
		
		super().__init__('dd', *args, block_id=NAMED_LIST_KEY_ID, next_blocks=next_blocks, **kwargs)

class named_list(TextTag):
	def __init__(self, items: Dict[str | Block | Tuple[Block], str | Block | List[Block]], *args, **kwargs) -> None:
		super().__init__(
			'dl', 
			*args, 
			block_id=NAMED_LIST_ID, 
			next_blocks=list(chain(*zip(
				map(_ordered_list_key, items.keys()), 
				map(_ordered_list_value, items.values())
			))),
			**kwargs
		)

	def __repr__(self) -> str:
		"""
		Shows information about the useful attributes of the object when printed
		Any attribute with length is only shown when length > 0
		The id is not shown
		For the class attributes of type string, keep up to 15 characters max, and if the string is longer than that, add an ellipsis
		"""
		return "<NamedList>"
