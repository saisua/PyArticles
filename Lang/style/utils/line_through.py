from typing import *

from Lang.style.defaults import DEFAULT_LINE_THROUGH

def line_through(block: Optional['Block'], *, overline=False, underline=False, through=False):
	if(block is None):
		return
	if(not any((overline, underline, through))):
		return block
	
	lines = []
	if(overline):
		lines.append('overline')
	if(underline):
		lines.append('line-through')
	if(through):
		lines.append('overline')

	
	line_through_key, line_through_value = DEFAULT_LINE_THROUGH
	
	block.style[line_through_key] = line_through_value.format(line_through=' '.join(lines))
	return block
	