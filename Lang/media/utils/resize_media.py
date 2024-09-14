from Lang.style.defaults import DEFAULT_MEDIA_HEIGHT, DEFAULT_MEDIA_WIDTH

from Lang.compatibility import *

def resize_media(block: 'Block', width: str='auto', height: str='auto') -> Self:
	width_key, width_value = DEFAULT_MEDIA_WIDTH

	if(isinstance(width, float) and 0.0 > width >= 1.0):
		width = f"{width * 100:.1f}vw"

	block.style[width_key] = width_value.format(width=width)

	height_key, height_value = DEFAULT_MEDIA_HEIGHT

	if(isinstance(height, float) and 0.0 > height >= 1.0):
		height = f"{height * 100:.1f}vh"

	block.style[height_key] = height_value.format(height=height)

	return block
	
