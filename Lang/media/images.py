from typing import *

from itertools import chain

from Lang.core.block import Block

from Lang.media.image_entry import Image_entry

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

class DelayedImages(Block):
	_images: 'Images'

	def __init__(self, images: 'Images'):
		self._images = images

		super().__init__()

	def __call__(self, document: 'Document', *args: Any, **kwargs: Any) -> None:
		if(not len(self._images._entries)):
			return

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
						text(f" {entry.caption}\n\n")
					])
					for entry in images
				]),
			])
		])


class Images:
	_entries: Dict[str, Image_entry]
	_rendered: Set[str]

	def __init__(self) -> None:
		self._entries = dict()
		self._rendered = set()

	def add(self, src: str, caption: str=None, *args: Any, **kwargs: Any) -> Image_entry:
		if(DEFAULT_REFERENCE_KEY not in kwargs):
			kwargs[DEFAULT_REFERENCE_KEY] = f"{DEFAULT_FIGURE_REF_PREFIX}{src}"

		entry = Image_entry(images=self, src=src, caption=caption, **kwargs)

		self._entries[src] = entry

		return entry

	def __call__(self, name: str) -> Optional[Image_entry]:
		return self._entries.get(name)

	def render(self, document: 'document') -> DelayedImages:
		return DelayedImages(self)
