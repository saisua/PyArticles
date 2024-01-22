from typing import *

from Lang.core.block import Block
from Lang.html.text_tag import TextTag
from Lang.text.text import _text as text
from Lang.id import TD_ID, TR_ID, TH_ID, TBODY_ID, TABLE_ID

from pandas import DataFrame


class _td(TextTag):
	def __init__(self, next_blocks: str | Block | List[Block], *args, **kwargs) -> None:
		if(isinstance(next_blocks, str)):
			next_blocks = text(next_blocks)
		
		super().__init__('td', *args, block_id=TD_ID, next_blocks=next_blocks, **kwargs)

class _th(TextTag):
	def __init__(self, next_blocks: str | Block | List[Block], *args, **kwargs) -> None:
		if(isinstance(next_blocks, str)):
			next_blocks = text(next_blocks)
		
		super().__init__('th', *args, block_id=TH_ID, next_blocks=next_blocks, **kwargs)

class _tr(TextTag):
	def __init__(self, next_blocks: List[str | Block | List[Block]], *args, cell_block=_td, **kwargs) -> None:
		if(not isinstance(next_blocks, (list, tuple))):
			next_blocks = cell_block(next_blocks)
		else:
			next_blocks = list(map(
				cell_block,
				next_blocks
			))
		
		super().__init__('tr', *args, block_id=TR_ID, next_blocks=next_blocks, **kwargs)

class _tbody(TextTag):
	def __init__(self, items: List[List[str | Block | List[Block]]], *args, **kwargs) -> None:
		super().__init__(
			'tbody', 
			*args, 
			block_id=TBODY_ID, 
			next_blocks=list(map(
				_tr, 
				items
			)), 
			**kwargs
		)

class table(TextTag):
	def __init__(self, items: List[List[str | Block | List[Block]]], *args, header: List[str | Block]=None,  **kwargs) -> None:
		if(header is None):
			next_blocks = _tbody(items=items)
		else:
			next_blocks = [
				_tr(header, cell_block=_th),
				_tbody(items=items)
			]

		super().__init__(
			'table', 
			*args, 
			block_id=TABLE_ID, 
			next_blocks=next_blocks,
			**kwargs
		)

	@staticmethod
	def from_pandas(df: DataFrame) -> TextTag:
		return table(
			header=df.columns,
			items=df.values,
		)