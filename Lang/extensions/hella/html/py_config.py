from Lang.html.base_tag import BaseTag, Block

from Lang.compatibility import *

class py_config(BaseTag):
	def __init__(self, next_blocks: List[Block] | None = None, *args, **kwargs) -> None:
		super().__init__('py-config', *args, next_blocks=next_blocks, **kwargs)