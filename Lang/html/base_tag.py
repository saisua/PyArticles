from Lang.core.block import Block, OpenBlock
from Lang.id import HEAD_ID

from Lang.style.utils.clear import clear
from Lang.style.utils.new_page import new_page
from Lang.style.utils.in_new_page import in_new_page
from Lang.style.utils.dont_split import dont_split
from Lang.style.utils.margin_right import margin_right
from Lang.style.utils.margin_left import margin_left

from Lang.compatibility import *

class _OpenBaseTag(OpenBlock):
	tag: object

	def __init__(self, head) -> None:
		self.tag = head

	async def __aenter__(self, *args, **kwargs):
		self.tag.__enter__()
		return self
	
	async def __aexit__(self, *args, **kwargs):
		self.tag.__exit__(None, None, None)

class BaseTag(Block):
	_tag: str

	def __init__(self, tag: str, *args, block_id: int=None, next_blocks: List[Block] | None = None, **kwargs) -> None:
		self._tag = tag

		super().__init__(*args, block_id=block_id, next_blocks=next_blocks, **kwargs)

	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> _OpenBaseTag:		
		args, kwargs = self._merge_args_kwargs(args, kwargs)

		return _OpenBaseTag(document.tag(self._tag, *args, **kwargs))
	
	clear=clear
	new_page = new_page
	in_new_page = in_new_page
	dont_split = dont_split
	margin_right = margin_right
	margin_left = margin_left

	def __repr__(self) -> str:
		if('id' in self._kwargs):
			return f"<{self._tag.capitalize()} id={self._kwargs['id']}>"
		return f"<{self._tag.capitalize()}>"
	
	@property
	def tag(self) -> str:
		return self._tag
	

	@property
	def id(self) -> int:
		if('id' not in self._kwargs):
			self._kwargs['id'] = f"{self._tag}{self._num_created_block}"
			
		return self._kwargs['id']