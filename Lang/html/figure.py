from Lang.html.base_tag import Block
from Lang.html.text_tag import TextTag
from Lang.media.media_tag import MediaTag
from Lang.id import FIGURE_ID

from Lang.compatibility import *

class figure(MediaTag):
	image: MediaTag
	caption: TextTag
	def __init__(self, image: MediaTag, caption: TextTag, *args, **kwargs) -> None:
		self.image = image
		self.caption = caption
		super().__init__('figure', *args, block_id=FIGURE_ID, next_blocks=[image, caption], **kwargs)
