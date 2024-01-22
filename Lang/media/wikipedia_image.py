from typing import *

import wikipedia

from Lang.media.media_tag import MediaTag
from Lang.id import IMG_ID

class wikipedia_image(MediaTag):
	def __init__(self, query: str, *args, image_index: int=0, **kwargs) -> None:
		inited = False
		try:
			search_results = wikipedia.search(query)

			if(len(search_results)):
				images = wikipedia.page(search_results[0]).images

				if(len(images) > image_index):
					super().__init__('img', *args, block_id=IMG_ID, src=images[image_index], **kwargs)
					inited = True
		except Exception as err:
			print(f"Wikipedia_image for \"{query}\" raised: {err}")

		if(not inited):
			super().__init__('img', *args, block_id=IMG_ID, **kwargs)
		

		if('margin' not in self.style):
			self.style['margin'] = '1em'