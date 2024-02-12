import asyncio
from typing import *
import os

from yattag import Doc

import aiofiles

from Lang.core.block import Block, OpenBlock
from Lang.html.html import html
from Lang.html.head import head
from Lang.html.body import body
from Lang.style.stylesheet import stylesheet
from Lang.html.script import script

from Lang.i18n.traductions import traductions

from Lang.defaults import DEFAULT_STATIC_FOLDER

class Document:
	path: str
	doc: Doc
	_blocks: List[Block]

	lang: str
	_lang_data: traductions

	def __init__(
				 self, 
				 path: str, 
				 *args, 
				 lang: str='en',
				 stylesheets: List[str]=['style.css', 'print.css'], 
				 scripts: List[str]=[],
				 **kwargs
		) -> None:
		self.path = path
		doc, tag, text, line = Doc(*args, **kwargs).ttl()

		self.doc = doc
		self.tag = tag
		self.text = text
		self.line = line

		valid_stylesheets = []
		for css_stylesheet in stylesheets:
			if(os.path.exists(os.path.join(path, DEFAULT_STATIC_FOLDER, css_stylesheet))):
				valid_stylesheets.append(css_stylesheet)
		valid_scripts = []
		for js_script in scripts:
			if(os.path.exists(os.path.join(path, DEFAULT_STATIC_FOLDER, js_script))):
				valid_scripts.append(js_script)
		
		_head = head()
		for filename in valid_scripts:
			_head += script(filename=filename)
		for filename in valid_stylesheets:
			_head += stylesheet(filename=filename)
		
		self.body = body()
		if(len(_head._next)):
			self._blocks = [html([_head, self.body])]
		else:
			del _head
			self._blocks = [html(self.body)]

		self.lang = lang
		self._lang_data = traductions(lang=lang)

	tag: Callable
	text: Callable
	line: Callable

	def __getitem__(self, id: int) -> Optional[Block]:
		for block in self._blocks:
			if(id == block._id): 
				return block
			
			if(id in block):
				return block[id]
	
	async def _build_doc(self) -> str:
		from Lang.text.text import _text

		open_block_queue: List[OpenBlock] = []
		block_queue: List[List[Block]] = [self._blocks]

		# Iterate over all to-be-opened blocks
		while(len(block_queue)):
			# If we have opened all children blocks
			if(len(block_queue[-1]) == 0):
				# If we have at least one open block to close
				if(len(open_block_queue)):
					# We close it
					await open_block_queue.pop(-1).__aexit__()
				# And we remove the child-less block
				block_queue.pop(-1)
				
				continue

			# We get the first child of the last
			# non-childless block in block_queue
			block = block_queue[-1].pop(0)

			if(isinstance(block, str)):
				block = _text(block)
			elif(block is None):
				continue

			# And we open it
			open_block = block(self)
			
			new_blocks: List[Block] = list()
			if(block._next):
				new_blocks.extend(block._next)
			
			if(open_block is not None):
				if(not isinstance(open_block, (list, tuple))):
					open_block = [open_block]
				
				# We will iterate over all the results
				sub_blocks_queue = list(open_block)
				while(len(sub_blocks_queue)):
					sub_block = sub_blocks_queue.pop()

					if(isinstance(sub_block, (list, tuple))):
						sub_blocks_queue.extend(sub_block)
					elif(isinstance(sub_block, Block)):
						new_blocks.append(sub_block)
					elif(isinstance(sub_block, OpenBlock)):
						await sub_block.__aenter__()
						if(block._next):
							open_block_queue.append(sub_block)
						else:
							await sub_block.__aexit__()

			if(len(new_blocks)):
				block_queue.append(new_blocks)

		if(len(open_block_queue)):
			await asyncio.gather(*(
				sub_open_block.__aexit__()
				for sub_open_block in open_block_queue
			))

		return self.doc.getvalue()

	async def render(self) -> str:
		return await self._build_doc()

	async def store(self, output_path: str, output_fname: str, *, doc_str: Optional[str]=None) -> None:
		if(doc_str is None):
			doc_str = await self.render()
		
		async with aiofiles.open(os.path.join(output_path, output_fname), 'w+') as f:
			await f.write(doc_str)

	@property
	def keywords(self):
		return self.LangKeyWords(self)

	class LangKeyWords:
		def __init__(self, doc: 'Document'):
			for kw, value in doc._lang_data.items():
				setattr(self, kw, value)
