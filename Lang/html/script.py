from Lang.core.block import Block, OpenBlock
from Lang.defaults import DEFAULT_STATIC_FOLDER
from Lang.id import LINK_SCRIPT_ID
from Lang.html.plain import plain

from Lang.compatibility import *

class _OpenScript(OpenBlock):
	tag: object

	def __init__(self, head) -> None:
		self.tag = head

	async def __aenter__(self, *args, **kwargs):
		self.tag.__enter__()
		return self
	
	async def __aexit__(self, *args, **kwargs):
		self.tag.__exit__(None, None, None)

class script(Block):
	filename: Optional[str]
	_defer: bool
	_type: Optional[str]
	
	def __init__(self, next_blocks: List[Block] | None = None, *args, filename: Optional[str]=None,  defer: bool=False, type:str=None, **kwargs) -> None:
		self.filename = filename
		self._defer = defer
		self._type = type

		if (not isinstance(next_blocks, (list, tuple))):
			next_blocks = [next_blocks]

		super().__init__(*args, block_id=LINK_SCRIPT_ID, next_blocks=list(map(plain, next_blocks)), **kwargs)

	def __repr__(self) -> str:
		return f"<Script filename={self.filename!r} defer={self._defer} type={self._type!r}>"

	def __call__(self, doc: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> None:
		tag_str: str
		if(self._defer):
			tag_str = 'script defer'
		else:
			tag_str = 'script'

		tag_attrs = {}

		if(self.filename is not None):
			if(self.filename.startswith('http') or self.filename.lstrip('.').startswith('/')):
				tag_attrs['src'] = self.filename
			else:
				tag_attrs['src'] = f'{DEFAULT_STATIC_FOLDER}/{self.filename}'

		if(self._type is not None):
			tag_attrs['type'] = self._type

		return _OpenScript(doc.tag(tag_str, **tag_attrs))
