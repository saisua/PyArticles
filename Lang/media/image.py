from typing import *

import os
from Lang.html.figure import figure
from Lang.html.figcaption import figcaption

from Lang.media.media_tag import MediaTag
from Lang.defaults import DEFAULT_STATIC_FOLDER
from Lang.id import IMG_ID
from Lang.text.text import _text

class _image(MediaTag):
	def __init__(self, src: str, *args, caption: Optional[str]=None, **kwargs) -> None:
		if(not src.lower().startswith('http')):
			src = os.path.join(DEFAULT_STATIC_FOLDER, src)

		super().__init__('img', *args, block_id=IMG_ID, src=src, **kwargs)

		if('margin' not in self.style):
			self.style['margin'] = '1em'

def image(src: str, *args, caption: Optional[str]=None, **kwargs):
	if(caption is None):
		return _image(src, *args, **kwargs)
	
	if(isinstance(caption, str)):
		caption = _text(caption)

	return figure(
		_image(src),
		figcaption(caption),
		*args, **kwargs
	)
