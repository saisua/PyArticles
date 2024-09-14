from typing import *

from Lang.compatibility import Any
from Lang.html.base_tag import _OpenBaseTag, BaseTag, Block
from Lang.id import BODY_ID

from Lang.text.text import _text

from Lang.compatibility import *

class body(BaseTag):
	_replacements: Dict[str, Any]

	def __init__(self, next_blocks: List[Block] | None = None, *args, replacements: Dict[str, Any]={}, **kwargs) -> None:
		self._replacements = replacements
		
		super().__init__('body', *args, block_id=BODY_ID, next_blocks=next_blocks, **kwargs)

	def __call__(self, document: 'Document', *args: Any, mode: str | int = None, **kwargs: Any) -> _OpenBaseTag:
		# Find any plain string and convert it to _text
		for block_n, next_block in enumerate(self._next):
			if(isinstance(next_block, str)):
				self._next[block_n] = _text(next_block, replacements=self._replacements)

		return super().__call__(document, *args, mode=mode, **kwargs)
