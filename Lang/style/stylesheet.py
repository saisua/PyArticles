from Lang.core.block import Block
from Lang.defaults import DEFAULT_STATIC_FOLDER
from Lang.id import LINK_STYLESHEET_ID

from Lang.compatibility import *

class stylesheet(Block):
	filename: str
	def __init__(self, next_blocks: List[Block] | None = None, *args, filename: str, **kwargs) -> None:
		self.filename = filename
		super().__init__(*args, block_id=LINK_STYLESHEET_ID, next_blocks=next_blocks, **kwargs)

	def __call__(self, doc: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> None:
		tag = doc.tag('link', rel='stylesheet', href=f'{DEFAULT_STATIC_FOLDER}/{self.filename}')
		tag.__enter__()
		tag.__exit__(None, None, None)
