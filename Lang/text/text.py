import re

from Lang.html.base_tag import Block
from Lang.html.text_tag import TextTag

from Lang.html.span import span
from Lang.html.div import div

from Lang.id import TEXT_ID

from Lang.style.utils.enable_newlines_text import enable_newlines_text

from Lang.compatibility import *

# Matches any newline character that is not preceeded by a newline character
lone_nl_cleanup_re: re.Pattern = re.compile(r"([^\n]|^)\n([^\n]|$)")
# Matches any sequence of one or more whitespace characters
space_cleanup_re: re.Pattern = re.compile(r"[ \t]+")
# Matches any sequence of two or more newline characters
nl_cleanup_re: re.Pattern = re.compile(r"\n{2}")

class _text(Block):
	text: str
	replacements: Dict

	_apply_formatting: bool
	_format_args: Tuple[str, ...]
	_format_kwargs: Dict[str, str]

	_called: bool=False

	def __init__(self, text: str, replacements: Dict={}, *args, next_blocks: List[Block] | None = None, apply_formatting: bool=True, **kwargs) -> None:
		self.text = text
		self.replacements = replacements

		self._apply_formatting = apply_formatting
		self._format_args = tuple()
		self._format_kwargs = dict()

		super().__init__(*args, block_id=TEXT_ID, next_blocks=next_blocks, **kwargs)

	def __repr__(self) -> str:
		"""
		Shows information about the useful attributes of the object when printed
		Any attribute with length is only shown when length > 0
		The id is not shown
		"""
		data = []

		if(self.text):
			if(isinstance(self.text, str) and len(self.text) > 15):
				data.append(f"text={self.text[:15]}...")
			else:
				data.append(f"text={self.text!r}")
		if(len(self.style) > 0):
			data.append(f"style={self.style!r}")

		return f"<Text{' ' if len(data) else ''}{''.join(data)}>"


	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> None:
		if(self._called):
			return
	
		rendered_text = self.render()

		if(isinstance(rendered_text, str)):
			document.text(rendered_text)
		elif(not self._called and isinstance(rendered_text, (list, tuple))):
			new_next = []
			for sub_block in rendered_text:
				if(isinstance(sub_block, str)):
					new_next.append(_text(sub_block))
				else:
					new_next.append(sub_block)

			self._next = [*new_next, *self._next]
		self._called = True

	def render(self):
		if (self._apply_formatting):
			return self._formatted_text(self.text)
		return self.text

	def _formatted_text(self, text: str) -> str:
		"""
		Formats the given text by applying cleanup formatting, replacing curly braces, and applying format arguments and keyword arguments.
		If there are any replacements defined, the text is further formatted with those replacements.
		
		:param text: The text to be formatted.
		:type text: str
		:return: The formatted text.
		:rtype: str
		"""
		text = self._cleanup_format(text)
		text = text.replace('{', '{{').replace('}', '}}').format(*self._format_args, **self._format_kwargs)
		if(len(self.replacements)):
			text = self._replacement_format(text)
		return text

	def _cleanup_format(self, text: str) -> str:
		"""
		Cleans up the given text by removing any duplicate newline characters, removing any newline characters that are not preceeded by a newline character, and replacing any sequences of whitespace characters with a single space character.
		
		:param text: The text to be cleaned up.
		:type text: str
		:return: The cleaned up text.
		:rtype: str
		"""
		# Replace any newline characters that are not preceeded by a newline character with an empty string
		text = lone_nl_cleanup_re.sub(
			'\g<1>\g<2>',
			# Replace any sequences of whitespace characters with a single space character
			space_cleanup_re.sub(
				' ',
				text
			)
		)
		
		# Replace any duplicate newline characters with a single newline character
		text = nl_cleanup_re.sub(
			'\n',
			text
		)
		
		return text

	def _replacement_format(self, text: str) -> Union[str, list]:
		secondary_queue = []
		text_queue = [text]

		replacements = dict(reversed(sorted(
			self.replacements.items(),
			key=lambda tup: len(tup[0])
		)))

		for token, replacement in replacements.items():
			for text in text_queue:
				if(not isinstance(text, str)):
					secondary_queue.append(text)
					continue

				split_text = text.split(token)
				for n, split in enumerate(split_text):
					if(n):
						secondary_queue.append(replacement)
					secondary_queue.append(split)

			text_queue, secondary_queue = secondary_queue, text_queue
			secondary_queue.clear()

		if(len(text_queue) == 1):
			return text_queue[0]
		return text_queue

	def format(self, *args, **kwargs):
		self._format_args = args
		self._format_kwargs = kwargs
	
def text(text: str, replacements: Dict={}, *args, next_blocks: List[Block] | None = None, format: Dict={'text-align': 'justify'}, tag: Block=div, **kwargs) -> TextTag:
	text = _text(text, replacements)

	if(format is not None):
		text.format(**format)

	if(next_blocks is None):
		next_blocks = text
	elif(isinstance(next_blocks, list)):
		next_blocks.insert(0, text)
	elif(isinstance(next_blocks, tuple)):
		next_blocks = [text, *next_blocks]
	else:
		next_blocks = [text, next_blocks]
	
	tag = tag(next_blocks, *args, **kwargs)
	enable_newlines_text(tag)

	return tag
