from Lang.style.defaults import DEFAULT_MEDIA_FLOAT, DEFAULT_MARGIN_LEFT, DEFAULT_MARGIN_RIGHT, DEFAULT_DISPLAY

from Lang.compatibility import *

def float_media(
		block: 'Block', 
		float: Union[
			Literal["left"],
			Literal["right"],
			Literal["none"],
			Literal["inherit"],
			Literal["center"],
		]=None,
		) -> Self:
	if(float == 'center'):
		margin_right_key, margin_right_value = DEFAULT_MARGIN_RIGHT
		
		block.style[margin_right_key] = margin_right_value.format(margin='auto')

		margin_left_key, margin_left_value = DEFAULT_MARGIN_LEFT
		
		block.style[margin_left_key] = margin_left_value.format(margin='auto')

		display_key, display_value = DEFAULT_DISPLAY
		
		block.style[display_key] = display_value.format(display='block')
		
	else:
		float_key, float_value = DEFAULT_MEDIA_FLOAT
		
		block.style[float_key] = float_value.format(float=float)

	return block
	
