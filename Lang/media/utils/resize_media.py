from typing import *

from Lang.style.defaults import DEFAULT_MEDIA_HEIGHT, DEFAULT_MEDIA_WIDTH

def resize_media(block: 'Block', width: str='auto', height: str='auto') -> Self:
	width_key, width_value = DEFAULT_MEDIA_WIDTH
	
	block.style[width_key] = width_value.format(width=width)

	height_key, height_value = DEFAULT_MEDIA_HEIGHT
	
	block.style[height_key] = height_value.format(height=height)

	return block
	