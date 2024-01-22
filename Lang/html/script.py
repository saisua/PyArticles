from typing import *

from Lang.core.block import Block
from Lang.defaults import DEFAULT_STATIC_FOLDER
from Lang.id import LINK_SCRIPT_ID

class script(Block):
	filename: str
	def __init__(self, next_blocks: List[Block] | None = None, *args, filename: str, **kwargs) -> None:
		self.filename = filename
		super().__init__(*args, block_id=LINK_SCRIPT_ID, next_blocks=next_blocks, **kwargs)

	def __call__(self, doc: 'Document', *args: Any, **kwargs: Any) -> None:
		tag = doc.tag('script', src=f'{DEFAULT_STATIC_FOLDER}/{self.filename}')
		tag.__enter__()
		tag.__exit__(None, None, None)