import asyncio
import os
import importlib

from yattag import Doc

import aiofiles

from Lang.plugin import Plugin

from Lang.core.block import Block, OpenBlock
from Lang.html.html import html
from Lang.html.head import head as Head
from Lang.html.body import body as Body
from Lang.style.stylesheet import stylesheet
from Lang.html.script import script

from Lang.i18n.traductions import traductions

from Lang.defaults import DEFAULT_STATIC_FOLDER

from Lang.compatibility import *

VERBOSE: Final[str] = False
VERBOSE_TAGS: Final[str] = False

class Document(Plugin):
	path: str
	doc: Doc
	_next: List[Block]
	_body: Body
	_head: Head

	_replacements: Dict[str, Any]

	_extensions: List[Callable[[Self], Any]]

	lang: str
	_lang_data: traductions

	_stylesheet_paths: List[str]
	_script_paths: List[str]

	_stylesheets: list = []
	_scripts: list = []
	_plugins: list[Plugin]

	VISUALIZING: int = 1
	RENDERING: int = 2

	# TODO: set default values as None and only set them in __init__
	# based on defaults.py
	def __init__(
				 self, 
				 *args, 
				 lang: str='en',
				 stylesheets: List[str]=['style.css', 'print.css'], 
				 scripts: List[str]=[],
				 extensions: List[Callable[[Self], Any]]=[],
				 replacements: Dict[str, Any]={},
				 plugins: List[Plugin]=[],
				 **kwargs
		) -> None:
		doc, tag, text, line = Doc(*args, **kwargs).ttl()

		self.doc = doc
		self.tag = tag
		self.text = text
		self.line = line
		self.asis = doc.asis

		self._stylesheet_paths = stylesheets
		self._script_paths = scripts
		self._plugins = plugins
		
		self._replacements = replacements

		self._body = None
		self._head = None

		self._next = []

		self._extensions = extensions

		self.lang = lang
		self._lang_data = traductions(lang=lang)

	def __repr__(self) -> str:
		return f"<Document path=\"{self.path}\" lang={self.lang} scripts={{{len(self._scripts)}}} stylesheets={{{len(self._stylesheets)}}}>"

	tag: Callable
	text: Callable
	line: Callable
	asis: Callable

	def __getitem__(self, id: int) -> Optional[Block]:
		for block in self._next:
			if(id == block._id): 
				return block
			
			if(id in block):
				return block[id]
	
	async def _build_doc(self, mode: str | int) -> str:
		from Lang.text.text import _text

		await asyncio.gather(*(
			extension(self, mode=mode)
			for extension in self._extensions
		))

		for _script in self._scripts:
			if(isinstance(_script, script)):
				self._head += _script
			elif(isinstance(_script, str)):
				self._head += script(filename=_script)
			else:
				raise ValueError(f"Unknown script type: {_script}")
		for _style in self._stylesheets:
			if(isinstance(_style, stylesheet)):
				self._head += _style
			elif(isinstance(_style, str)):
				self._head += stylesheet(filename=_style)
			else:
				raise ValueError(f"Unknown stylesheet type: {_style}")
		
		if(len(self._head._next) != 0):
			self._next.insert(0, html([self._head, self._body]))
		else:
			self._next.insert(0, html([self._body]))

		open_block_queue: List[List[OpenBlock]] = [[]]
		block_queue: List[List[Union[Block, str]]] = [self._next]

		if(VERBOSE): print(f"###\nSTART BUILD DOC: {len(self._next)} blocks\n###")

		# Iterate over all to-be-opened blocks
		while(len(block_queue)):
			if(VERBOSE): print(f"\n\n###\nNew iteration.\nRemaining blocks in queue: {len(block_queue)}\nRemaining blocks in group: {len(block_queue[-1])}\n"
								f"Remaining open block groups: {len(open_block_queue)}\nRemaining open block in group: {len(open_block_queue[-1])}\n")

			# If we have opened all children blocks
			if(len(block_queue[-1]) == 0):
				# If we have at least one open block to close
				if(len(open_block_queue[-1])):
					if(VERBOSE): print(f"Closing {len(open_block_queue[-1])} open blocks in position {len(open_block_queue)}\n"
										f" Closed open blocks: {', '.join(map(lambda x: type(x).__name__ if type(x).__name__ != '_OpenBaseTag' else f'_OpenBaseTag({x.tag.name})', open_block_queue[-1][::-1]))}")
					# We close them
					await asyncio.gather(*(
						open_block.__aexit__()
						for open_block in open_block_queue.pop(-1)[::-1]
					))
				else:
					if(VERBOSE): print(f"Removed empty open blocks in position {len(open_block_queue)}")
					open_block_queue.pop(-1)
				# And we remove the childless block
				if(VERBOSE): print(f"Removed empty blocks queued group in position {len(open_block_queue)}")
				block_queue.pop(-1)
				
				continue

			# We get the first child of the last
			# non-childless block in block_queue
			block = block_queue[-1].pop(0)
			if(block is None):
				if(VERBOSE): print("Got None block: Discarded")
				continue
			elif(isinstance(block, str)):
				if(VERBOSE): print(f"Got str block: {block}")
				block = _text(block, replacements=self._replacements)
				block(self, mode=mode)

				if(not block._next):
					if(VERBOSE): print(" Not generated next blocks")
					continue
				if(VERBOSE): print(f" Got {len(block._next)} generated next blocks")

			if(isinstance(block, (list, tuple)) and len(block) != 1):
				if(VERBOSE): print(f"Got {len(block)} blocks.\nRe-queued {len(block)-1} blocks")
				block_queue[-1].extend(block[1:])
				block = block[0]


			new_blocks: List[Block] = list()
			new_open_blocks: List[OpenBlock] = list()

			if(VERBOSE): print(f"Got {type(block).__name__} block", flush=False)
			if(VERBOSE_TAGS): print(f"{' '*(len(open_block_queue))}{block!r}")
			# And we open it
			sub_blocks_queue = block(self, mode=mode)

			# _next can change after the block.__call__
			if(block._next):
				new_blocks.extend(block._next.copy())

			if(sub_blocks_queue is not None):
				if(not isinstance(sub_blocks_queue, (list, tuple))):
					if(VERBOSE): print(f" Got 1 {type(sub_blocks_queue).__name__} open block")
					sub_blocks_queue = [sub_blocks_queue]
				else:
					if(VERBOSE): print(f" Got {len(sub_blocks_queue)} open blocks")
					sub_blocks_queue = list(sub_blocks_queue)

				# We will iterate over all the results
				while(len(sub_blocks_queue)):
					sub_block = sub_blocks_queue.pop()

					if(isinstance(sub_block, (list, tuple))):
						if(VERBOSE): print(f"   Got {len(sub_block)} open sub-blocks")
						sub_blocks_queue.extend(sub_block)
					elif(isinstance(sub_block, (Block, str))):
						if(VERBOSE): print(f"  Got 1 Block open sub-block")
						new_blocks.append(sub_block)
					elif(isinstance(sub_block, OpenBlock)):
						if(VERBOSE): print(f"  Got 1 OpenBlock open sub-block")
						new_open_blocks.append(sub_block)
					else:
						raise ValueError(f"  Got an unrecognized sub-block of type {type(sub_block)}")

			if(len(new_open_blocks)):
				await asyncio.gather(*(
					sub_open_block.__aenter__()
					for sub_open_block in new_open_blocks
				))

				if(VERBOSE): print(f" Added a new open_blocks group of length {len(new_open_blocks)}")
				open_block_queue.append(new_open_blocks)

				if(len(new_blocks)):
					if(VERBOSE): print(f" Added a new blocks group of length {len(new_blocks)}")
					block_queue.append(new_blocks)
				else:
					if(VERBOSE): print(" Added a new empty blocks group")
					block_queue.append([])

			elif(len(new_blocks)):
				if(VERBOSE): print(f" Added a new blocks group of length {len(new_blocks)}")
				block_queue.append(new_blocks)

				if(VERBOSE): print(" Added a new empty open blocks group")
				open_block_queue.append([])

			assert len(block_queue) == len(open_block_queue), f"{len(block_queue)} block queue groups. {len(open_block_queue)} open block queue groups"

		if(len(open_block_queue)):
			if(VERBOSE): print(f"Closing remaining {len(open_block_queue)} open_block groups")
			await asyncio.gather(*(
				open_block.__aexit__()
				for sub_open_block in open_block_queue
				if len(sub_open_block)
				for open_block in sub_open_block
			))

		return self.doc.getvalue()

	async def _new_build_doc(self) -> str:
		return self.doc.getvalue()

	def attach(self, gen_fn: Callable[[Self], Any]) -> None:
		async def doc_attach_wrapper(output_path: str, output_fname: str):
			if(not self._is_plugin_setup):
				await asyncio.gather(
					self.setup(output_path, output_fname, doc=self),
					*(
						plugin.setup(output_path, output_fname, doc=self)
						for plugin in self._plugins
					)
				)
				self._is_plugin_setup = True
			else:
				await asyncio.gather(
					self.clear(),
					*(
						plugin.clear()
						for plugin in self._plugins
					)
				)
			
			doc = await gen_fn(self)

			if doc is None:
				doc = self

			doc.body
			doc.head

			render_plugin_coros = (
				plugin.render(doc, mode=Document.RENDERING)
				for plugin in self._plugins
			)
			for rendered_plugin in await asyncio.gather(*render_plugin_coros):
				doc._body += rendered_plugin

			await doc.store(output_path, output_fname)

		return doc_attach_wrapper
	
	async def setup(self, output_path, output_fname, doc: "Document") -> None:
		self.path = output_path
		
		valid_stylesheets = []
		for css_stylesheet in self._stylesheet_paths:
			if(os.path.exists(os.path.join(self.path, DEFAULT_STATIC_FOLDER, css_stylesheet))):
				valid_stylesheets.append(css_stylesheet)

		self._stylesheets = valid_stylesheets

		valid_scripts = []
		for js_script in self._script_paths:
			if(os.path.exists(os.path.join(self.path, DEFAULT_STATIC_FOLDER, js_script))):
				valid_scripts.append(js_script)
		
		self._scripts = valid_scripts

		self._is_plugin_setup = True	

	async def clear(self) -> None:
		self._body = None
		self._head = None
		self._next.clear()

	async def render(self, mode: str | int = VISUALIZING) -> str:
		return await self._build_doc(mode=mode)

	async def store(self, output_path: str, output_fname: str, *, doc_str: Optional[str]=None, render_mode: str | int=RENDERING) -> None:
		if(doc_str is None):
			doc_str = await self.render(mode=render_mode)
		
		async with aiofiles.open(os.path.join(output_path, output_fname), 'w+') as f:
			await f.write(doc_str)

	def add_stylesheet(self, filename: Optional[str], *args, **kwargs) -> None:
		self._stylesheets.append(stylesheet(*args, filename=filename, **kwargs))

	def add_script(self, filename: Optional[str], *args, **kwargs) -> None:
		self._scripts.append(script(*args, filename=filename, **kwargs))

	def add_extension(self, extension: Callable[[Self], Any]) -> None:
		self._extensions.append(extension)

	def add_plugin(self, plugin: Plugin) -> None:
		self._plugins.append(plugin)

	def import_part(self, 
					part_rel_path: str, 
					locals: dict={}, 
					globals: dict={}, 
					*args,
					callable_name: str="generate",
					**kwargs,
		) -> Any:
		spec = importlib.util.spec_from_file_location(
			"m", 
			os.path.join(self.path, part_rel_path)
		)

		if(spec is None):
			raise FileNotFoundError(f"Could not import \"{part_rel_path}\"")

		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)

		return getattr(module, callable_name)(self, *args, **{**globals, **locals, **kwargs})

	@property
	def keywords(self):
		return self.LangKeyWords(self)

	@property
	def body(self) -> Body:
		if(self._body is None):
			self._body = Body(next_blocks=self._next, replacements=self._replacements)

		return self._body
	
	@property
	def head(self) -> Head:
		if(self._head is None):
			self._head = Head()

		return self._head


	class LangKeyWords:
		def __init__(self, doc: 'Document'):
			for kw, value in doc._lang_data.items():
				setattr(self, kw, value)
