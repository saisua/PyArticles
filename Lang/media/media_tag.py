from Lang.html.base_tag import BaseTag

from Lang.media.utils.resize_media import resize_media
from Lang.media.utils.float_media import float_media

from Lang.compatibility import *

class MediaTag(BaseTag):
	resize = resize_media
	float = float_media
