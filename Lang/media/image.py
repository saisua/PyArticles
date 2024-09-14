import os
from Lang.html.figure import figure
from Lang.html.figcaption import figcaption

from Lang.media.media_tag import MediaTag
from Lang.defaults import DEFAULT_STATIC_FOLDER
from Lang.id import IMG_ID
from Lang.text.text import _text

from Lang.compatibility import *

class _image(MediaTag):
	def __init__(self, src: str, *args, caption: Optional[str]=None, **kwargs) -> None:
		if(not src.lower().startswith('http')):
			src = os.path.join(DEFAULT_STATIC_FOLDER, src)

		super().__init__('img', *args, block_id=IMG_ID, src=src, **kwargs)

		if('margin' not in self.style):
			self.style['margin'] = '1em'

	def __repr__(self) -> str:
		"""
		Shows information about the useful attributes of the object when printed
		Any attribute with length is only shown when length > 0
		The id is not shown
		For the class attributes of type string, keep up to 15 characters max, and if the string is longer than that, add an ellipsis
		"""
		return "<Image>"

def image(src: str, *args, caption: Optional[str]=None, **kwargs):
	if(caption is None):
		return _image(src, *args, **kwargs)
	
	child_style = {
		'width': '100%',
		'height': 'auto',
	}
	return figure(
		_image(src, style=child_style),
		figcaption(caption, style=child_style),
		*args, **kwargs
	)
