from Lang.core import Block
from Lang.id import HTML_ID

from Lang.compatibility import *

class plain(Block):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__(*args, next_blocks=next_blocks, **kwargs)
		
	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> None:
		for plain in self._next:
			if (isinstance(plain, str)):
				document.asis(plain)
		self._next.clear()

	def __repr__(self) -> str:
		return "<plain>"
