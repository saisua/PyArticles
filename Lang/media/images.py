from itertools import chain

import os
import tempfile
import pickle as pkl
from typing import Coroutine

from plotly import graph_objects as go


from Lang.core.block import Block

from Lang.media.image_entry import Image_entry

from Lang.media.media_tag import MediaTag

from Lang.plugin import Plugin
from Lang.html.text_tag import TextTag

from Lang.html.h import h
from Lang.html.b import b
from Lang.html.a import a
from Lang.html.div import div
from Lang.html.span import span
from Lang.style.new_page import new_page
from Lang.text.text import _text as text

from Lang.lists.unordered import unordered_list

from Lang.defaults import DEFAULT_FIGURE_REF_PREFIX, DEFAULT_REFERENCE_KEY

from Lang.compatibility import *

class DelayedImages(Block):
	_images: 'Images'
	_called: bool=False

	def __init__(self, images: 'Images'):
		self._images = images

		super().__init__()

	def __repr__(self) -> str:
		"""
		Shows information about the useful attributes of the object when printed
		Any attribute with length is only shown when length > 0
		The id is not shown
		For the class attributes of type string, keep up to 15 characters max, and if the string is longer than that, add an ellipsis
		"""
		return f"<DelayedImages images={self._images!r}>"

	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> None:
		if(self._called or not len(self._images._entries)):
			return
		self._called = True

		images = sorted((
				entry
				for entry in self._images._entries.values()
				if entry.src in self._images._rendered
			),
			key=lambda entry: entry.num
		)

		self._next.extend([
			new_page(),
			div([
				h(1, text(document._lang_data['FIGURES'])),
				unordered_list([
					span([
						a(
							b(f"{document._lang_data['FIGURE']} {entry.num}:"),
							href=f"#{entry._kwargs[DEFAULT_REFERENCE_KEY]}"
						),
						*entry._parse_caption(entry.caption),
					])
					for entry in images
				]),
			])
		])

class Images(Plugin):
	__tempfiles_path: str
	__tempfiles: Dict[str, str]
	_entries: Dict[str, Image_entry]
	_rendered: Set[str]

	_static_folder: str
	_static_path: str = None

	def __init__(self, static_folder: str = 'static') -> None:
		self._entries = dict()
		self._rendered = set()
		self.__tempfiles = None
		self.__tempfiles_path = None

		self._static_folder = static_folder

	def __repr__(self) -> str:
		return '<Images>'

	async def setup(self, output_path, output_fname, doc: 'Document') -> None:
		self.static_path = os.path.join(output_path, self._static_folder)
		self._is_plugin_setup = True	

	async def clear(self):
		self._entries.clear()
		self._rendered.clear()

	async def render(self, document: 'document', mode: str | int=None) -> DelayedImages:
		return DelayedImages(self)

	def _flush(self):
		self.__tempfiles.clear()

	def add(self, src: str, /, caption: str=None, *args: Any, **kwargs: Any) -> Image_entry:
		if(DEFAULT_REFERENCE_KEY not in kwargs):
			kwargs[DEFAULT_REFERENCE_KEY] = f"{DEFAULT_FIGURE_REF_PREFIX}{src}"

		entry = Image_entry(images=self, src=src, caption=caption, **kwargs)

		self._entries[src] = entry

		return entry

	def add_render(self, src: str, /, caption: str=None, *args: Any, document: 'Document', **kwargs: Any) -> MediaTag:
		return self.add(src, caption=caption, *args, **kwargs).render(document=document)

	def __call__(self, name: str) -> Optional[Image_entry]:
		return self._entries.get(name)

	def from_plotly(self, fig: go.Figure, /, caption: str=None, *args, **kwargs) -> Image_entry:
		if(self._static_path is None):
			raise ValueError("Images static_path is not set. You can't generate images from plotly unless you specify it")

		if(self.__tempfiles is None):
			if(os.path.exists(self.__tempfiles_path)):
				with open(self.__tempfiles_path, 'rb+') as f:
					self.__tempfiles = pkl.load(f)
			else:
				self.__tempfiles = dict()

		id = kwargs.get('id', caption or f"__Fig{len(self._entries)}")

		tmp_filename: str = self.__tempfiles.get(id)

		if(tmp_filename is None):
			with tempfile.NamedTemporaryFile(delete=False, suffix='.png', dir=self._static_path) as f:
				tmp_filename = f.name
				self.__tempfiles[id] = tmp_filename

			with open(self.__tempfiles_path, 'wb+') as f:
				pkl.dump(self.__tempfiles, f)

		fig.write_image(tmp_filename)

		return self.add(tmp_filename.split(os.sep)[-1], caption=caption, *args, **kwargs)

	@property
	def static_path(self) -> str:
		return self._static_path

	@static_path.setter
	def static_path(self, new_static_path: str) -> None:
		self._static_path = new_static_path.rstrip('/')
		self.__tempfiles_path = f"{self._static_path}/.images_tempfiles_registry"

