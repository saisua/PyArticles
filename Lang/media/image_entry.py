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

from Lang.compatibility import *

class DelayedImageEntryReference(Block):
	_entry: 'Image_entry'
	_called: bool = False

	def __init__(self, entry: 'Image_entry'):
		self._entry = entry

		super().__init__()

	def __repr__(self) -> str:
		"""
		Shows information about the useful attributes of the object when printed
		Any attribute with length is only shown when length > 0
		The id is not shown
		For the class attributes of type string, keep up to 15 characters max, and if the string is longer than that, add an ellipsis
		"""
		return f"<DelayedImageEntryReference: _entry={self._entry!r}>"

	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any):
		if(self._called):
			return
		self._called = True

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

		if(num is None):
			num = len(self.images._rendered)

		self.num = num

		self.images._rendered.add(self.src)

		super().__init__(tag='div', **kwargs)

	def __repr__(self) -> str:
		"""
		Shows information about the useful attributes of the object when printed
		Any attribute with length is only shown when length > 0
		The id is not shown
		For the class attributes of type string, keep up to 15 characters max, and if the string is longer than that, add an ellipsis
		"""
		return f"<Image_entry num={self.num!r}, src={self.src!r}, caption={self.caption!r}>"

	def _parse_caption(self, caption, document: Optional['Document']=None) -> list:
		if(caption is None):
			return []
		
		elif(isinstance(caption, str)):
			if(document is not None):
				replacements = document._replacements
			else:
				replacements = {}
			
			return [text(f" {caption}", replacements=replacements)]
		else:
			return [text(' '), caption]

	def render(self, document: 'Document', mode: str | int=None) -> MediaTag:
		if(self.num is None):
			self.num = len(self.images._rendered)
			self.images._rendered.add(self.src)

		return image(
			src=self.src,
			caption=span([
				b(
					text(f"{document._lang_data['FIGURE']} {self.num}:"),
					id=f"{DEFAULT_FIGURE_REF_PREFIX}{self.src}",
				),
				*self._parse_caption(self.caption, document)
			]),
			style=self.style
		)

	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> DelayedImageEntryReference:
		return DelayedImageEntryReference(self)

