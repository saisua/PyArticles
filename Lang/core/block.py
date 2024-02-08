from typing import *

import asyncio
import os
import binascii
from itertools import chain

from Lang.defaults import DEFAULT_GOTO_REFERENCE_KEY, DEFAULT_REFERENCE_KEY

class MergedOpenBlock:
	_open_blocks: List['OpenBlock']

	def __init__(self, blocks: List['OpenBlock']) -> None:
		self._open_blocks = list(blocks)

	def __add__(self, open_block: 'OpenBlock') -> Self:
		self._open_blocks.append(open_block)

		return self
	
	def __iadd__(self, open_block: 'OpenBlock') -> Self:
		self._open_blocks.append(open_block)

		return self
	

	async def __aenter__(self, *args, **kwargs) -> Self:
		asyncio.gather(*(
			open_block.__aenter__(*args, **kwargs)
			for open_block in self._open_blocks
		))
		return self

	async def __aexit__(self, *args, **kwargs):
		asyncio.gather(*(
			open_block.__aexit__(*args, **kwargs)
			for open_block in self._open_blocks
		))

class OpenBlock:
	_block: 'Block'

	async def __aenter__(self, *args, **kwargs) -> Self:
		return self

	async def __aexit__(self, *args, **kwargs):
		...

	def __add__(self, open_block: 'OpenBlock') -> MergedOpenBlock:
		return MergedOpenBlock([self, open_block])

class Block:
	_id: int
	_fn: Callable
	_args: Tuple
	_kwargs: Dict[str, Any]

	style: Dict[str, str]

	_next: List['Block']
	_children: Set[int]

	def __init__(self, fn=None, *args, block_id: int=None, next_blocks: Optional[List['Block']]=None, **kwargs) -> None:
		self._id = block_id

		self.style = kwargs.pop('style', dict())

		href = kwargs.get(DEFAULT_GOTO_REFERENCE_KEY, '')
		if(isinstance(href, Block)):
			kwargs[DEFAULT_GOTO_REFERENCE_KEY] = href.reference

		self._fn = fn
		self._args = args
		self._kwargs = kwargs

		self._children = set()
		if next_blocks:
			if(not isinstance(next_blocks, (list, tuple))):
				next_blocks = [next_blocks]
				
			self._next = list(filter(None, next_blocks))
			for block in self._next:
				if(isinstance(block, str)):
					from Lang.text.text import _text
					block = _text(block)
				self._children.add(block._id)
				self._children.update(block._children)
		else:
			self._next = list()

	def _merge_args_kwargs(self, args, kwargs, *, style_to_str: bool=True) -> Tuple[Tuple, Dict[str, Any]]:
			if(len(self._args) > len(args)):
				args = chain(args, self._args[len(args):])
			kwargs.update(self._kwargs)

			if('style' not in kwargs and len(self.style)):
				if(style_to_str and isinstance(self.style, dict)):
					style = ';'.join((f"{k}:{v}" for k, v in self.style.items()))

					kwargs['style'] = style
				else:
					kwargs['style'] = self.style
				
			return args, kwargs

	# Implement hash

	def __call__(self, document: 'Document', *args: Any, **kwargs: Any) -> Optional[OpenBlock]:
		if(self._fn is not None):
			args, kwargs = self._merge_args_kwargs(args, kwargs)

			self._fn(document, *args, **kwargs)

		# return OpenBlock()
	
	def __getitem__(self, id: int) -> 'Block':
		if(id == self._id): 
			return self
		
		for block in self._next:
			if(id == block._id):
				return block
			if(id in block):
				return block[id]

	def __contains__(self, id: int) -> bool:
		return id in self._children
	
	def __next__(self) -> List['Block']:
		return self._next
	
	def __iter__(self) -> Generator['Block', None, None]:
		if(not self._next):
			return
		
		objs_queue: List['Block'] = self._next
		while(len(objs_queue)):
			obj = objs_queue.pop(0)

			yield obj
			
			if(not obj._next):
				continue

			objs_queue[:0] = obj._next

	
	def __add__(self, block: 'Block' | List['Block'] | Tuple['Block']) -> Self:
		if(block is None):
			return self

		if(isinstance(block, (list, tuple))):
			for sub_block in block:
				self.__add__(sub_block)
		elif(isinstance(block, str)):
			from Lang.text.text import text

			self.__add__(text(block))
		else:
			self._next.append(block)

		return self
	
	def __radd__(self, block: 'Block' | List['Block'] | Tuple['Block']) -> Self:
		return self.__add__(block)
	
	def reference_to(self, block: Union['Block', str]) -> Self:
		if(isinstance(block, Block)):
			self._kwargs[DEFAULT_GOTO_REFERENCE_KEY] = block.reference
		elif(isinstance(block, str)):
			self._kwargs[DEFAULT_GOTO_REFERENCE_KEY] = block
		else:
			raise ValueError("Reference is not a block nor a string")

		return self

	@property
	def reference(self) -> str:
		if(DEFAULT_REFERENCE_KEY in self._kwargs):
			return f'#{self._kwargs[DEFAULT_REFERENCE_KEY]}'
		
		name = binascii.b2a_hex(os.urandom(15)).decode()
		self._kwargs[DEFAULT_REFERENCE_KEY] = name
		return f'#{name}'
