import markdown

from Lang.core.block import Block, OpenBlock
from Lang.id import MARKDOWN_ID

from Lang.style.utils.clear import clear
from Lang.style.utils.new_page import new_page
from Lang.style.utils.in_new_page import in_new_page
from Lang.style.utils.dont_split import dont_split
from Lang.style.utils.margin_right import margin_right
from Lang.style.utils.margin_left import margin_left

from Lang.compatibility import *


def remove_min_indentation(text):
    # Split the text into lines
    lines = text.splitlines()

    # Find the minimum indentation by considering only non-empty lines
    min_indentation = min((len(line) - len(line.lstrip()) for line in lines if line.strip()), default=0)

    # Remove the minimum indentation from all lines
    adjusted_lines = [line[min_indentation:] if len(line) >= min_indentation else line for line in lines]

    # Join the adjusted lines back into a single string
    return '\n'.join(adjusted_lines)


class _OpenMarkdown(OpenBlock):
	data: str
	doc: 'Document'

	def __init__(self, data, doc) -> None:
		self.data = data
		self.doc = doc

	async def __aenter__(self, *args, **kwargs):
		self.doc.asis(self.data)
		return self
	
	async def __aexit__(self, *args, **kwargs):
		""""""
		pass

class markdown_text(Block):
	_data: str
	_extensions: list[str]

	def __init__(self, data: str, *args, next_blocks: List[Block] | None = None, extensions: list[str] = ['fenced_code'], **kwargs) -> None:
		self._data = data
		self._extensions = extensions
		super().__init__(*args, block_id=MARKDOWN_ID, next_blocks=next_blocks, **kwargs)

	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> _OpenMarkdown:		
		formatted_data = remove_min_indentation(self._data)

		html_data = markdown.markdown(formatted_data, output_format='html5', extensions=self._extensions)
		return _OpenMarkdown(html_data, document)
	
	def __repr__(self) -> str:
		if('id' in self._kwargs):
			return f"<{self._tag.capitalize()} id={self._kwargs['id']}>"
		return f"<{self._tag.capitalize()}>"
	
	@property
	def id(self) -> int:
		if('id' not in self._kwargs):
			self._kwargs['id'] = f"{self._tag}{self._num_created_block}"
			
		return self._kwargs['id']