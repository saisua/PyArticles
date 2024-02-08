from typing import *

from itertools import chain

from Lang.core.block import Block

from Lang.media.image import _image, image, figure
from Lang.media.media_tag import MediaTag

from Lang.html.text_tag import TextTag

from Lang.html.h import h
from Lang.html.b import b
from Lang.html.a import a
from Lang.html.div import div
from Lang.html.span import span
from Lang.style.new_page import new_page
from Lang.text.text import _text as text

from Lang.lists.unordered import unordered_list

from Lang.defaults import DEFAULT_FIGURE_REF_PREFIX

class DelayedImageEntryReference(Block):
	_entry: 'Image_entry'

	def __init__(self, entry: 'Image_entry'):
		self._entry = entry

		super().__init__()

	def __call__(self, document: 'Document', *args: Any, **kwargs: Any):
		self._next.append(
			a(f"{document._lang_data['FIGURE']} {self._entry.num}", href=self._entry.reference)
		)

# TODO: Refactor to ImageEntry
class Image_entry(MediaTag):
	images: object
	src: str
	caption: str
	num: int=None

	def __init__(self, images: object, src: str, *args, caption: str, num: int=None, **kwargs):
		self.images = images
		self.src = src
		self.caption = caption

		if(num is not None):
			self.images._rendered.add(self.src)

		self.num = num

		super().__init__(tag='div', **kwargs)

	def __call__(self, document: 'Document', *args: Any, **kwargs: Any) -> None:
		if(self.num is None):
			self.num = len(self.images._rendered)
			self.images._rendered.add(self.src)

		self._next.append(
			image(
				src=self.src,
				caption=span([
					b(
						text(f"{document._lang_data['FIGURE']} {self.num}: "),
						id=f"{DEFAULT_FIGURE_REF_PREFIX}{self.src}",
					),
					text(self.caption)
				]),
				style=self.style
			),
		)

	def render(self) -> DelayedImageEntryReference:
		return DelayedImageEntryReference(self)

