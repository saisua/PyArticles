from typing import *

import os

from Lang.media.media_tag import MediaTag
from Lang.defaults import DEFAULT_STATIC_FOLDER
from Lang.id import IMG_ID

class image(MediaTag):
	def __init__(self, src: str, *args, **kwargs) -> None:
		if(not src.lower().startswith('http')):
			src = os.path.join(DEFAULT_STATIC_FOLDER, src)

		super().__init__('img', *args, block_id=IMG_ID, src=src, **kwargs)

		if('margin' not in self.style):
			self.style['margin'] = '1em'