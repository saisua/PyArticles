from functools import partial
from typing import List, Any, Dict, Callable, Union, Tuple
from Lang.plugin import Plugin
from Lang.core.block import Block, OpenBlock
from Lang.html.base_tag import BaseTag

from Lang.html.div import div
from Lang.html.h import h
from Lang.html.a import a
from Lang.text.text import _text as text

from Lang.style.utils.margin_left import margin_left

from Lang.defaults import DEFAULT_REFERENCE_KEY

from Lang.compatibility import *

class DelayedIndex(BaseTag):
	_index: 'Index'
	def __init__(self, index: 'Index', *args, block_id: int = None, next_blocks: List[Block] | None = None, **kwargs) -> None:
		self._index = index

		super().__init__('div', *args, block_id=block_id, next_blocks=next_blocks, **kwargs)

	def __repr__(self) -> str:
		"""
		Shows information about the useful attributes of the object when printed
		Any attribute with length is only shown when length > 0
		The id is not shown
		"""
		return f"<DelayedIndex index={self._index!r}>"

	def __call__(self, document: 'Document', *args: Any, mode: str | int=None, **kwargs: Any) -> None:
		args, kwargs = self._merge_args_kwargs(args, kwargs, style_to_str=False)

		self._next.append(
			margin_left(
				div([
					h(1, text(document._lang_data["INDEX"])),
					*(
						margin_left(
							div(a(
								h(
									min(6, section_number.count('.') + 2), 
									text(f"{section_number}{self._index._sep}{section_name}"),
								),
								href=f"#{section_name}",
							)),
							f"{min(6, section_number.count('.'))*self._index._bleeding}%"
						)
						for section_number, section_name in self._index._section_names.items()
					)],
					*args, **kwargs
				),
				'5%'
		)	)

class IndexEntry(Block):
	_index: 'Index'

	_bleeding: int = 0

	_entry_text: str
	_entry_id: int
	_section: bool

	_entry_args: List[Any]
	_entry_kwargs: Dict[str, Any]
	_entry_transforms: List[Union[Callable, Tuple[str, List[Any], Dict[str, Any]]]]

	_render_cache = None

	def __init__(self, index: 'Index', entry_text: str, entry_id: int, section: list[int] = False, *args, bleeding: int = 0, transforms: List[Callable] = None, **kwargs):
		self._index = index

		self._bleeding = bleeding

		self._entry_text = entry_text
		self._entry_id = entry_id
		self._section = section

		self._entry_args = args
		self._entry_kwargs = kwargs
		self._entry_transforms = transforms or list()

	def __repr__(self) -> str:
		return f"<IndexEntry index={self._index!r} rendered={self.rendered!r}>"
	
	def __enter__(self):
		self._index.__enter__()
		self._section[-1] -= 1
		self._section.append(1)
		self.render()
		return self

	def __exit__(self, *args, **kwargs):
		self._index.__exit__(*args, **kwargs)
		self._section.pop(-1)

	def __call__(self, *args: Any, **kwds: Any) -> Any:
		return self.rendered(*args, **kwds)

	def __add__(self, block: Block | List[Block] | Tuple[Block]) -> Any:
		self.rendered.__add__(block)
		return self

	def render(self):
		if(self._section):
			section_number = '.'.join(map(str, self._section))

			self._index._section_names[section_number] = self._entry_text
		else:
			section_number = None

		entry = div(
			h(
				min(6, len(self._section)),
				text(self._index._style(section_number, self._entry_text, self._index._sep)),
				id=self._entry_id
			),
			*self._entry_args, 
			**self._entry_kwargs
		)

		for transform in self._entry_transforms:
			if (isinstance(transform, tuple)):
				getattr(entry, transform[0])(*transform[1], **transform[2])
			else:
				transform(entry)

		entry = margin_left(
			entry,
			f"{min(6, len(self._section) - 1)*(self._bleeding or self._index._bleeding)}%"
		)

		self._render_cache = entry

		return entry
	
	def clear(self, *args, **kwargs):
		self._entry_transforms.append(('clear', args, kwargs))
		return self

	@property
	def rendered(self):
		if (self._render_cache is None):
			self.render()

		return self._render_cache

	@property
	def _next(self):
		return self.rendered._next
	

def _default_style(section_number: Optional[str], section_name: Optional[str], sep: Optional[str]):
	if(section_number is None):
		return section_name

	if(sep is None):
		sep = ' '
	return f"{section_number}{sep}{section_name}"

class Index(Plugin):
	_section_names: Dict[str, str]
	_section: List[int]

	_bleeding: float
	_sep: str
	_style: Callable[[str, str, str], str]

	_styles: Dict[str, Callable[[str, str, str], str]] = {
		'default': _default_style
	}

	_kwargs: dict

	def __init__(self, *args, next_blocks: List[Block] | None = None, bleeding: float=1.5, sep: str='. ', style: str='default', **kwargs) -> None:
		self._section = [0]
		self._section_names = {}

		self._bleeding = 1.5
		self._sep = sep
		self._style = self._styles.get(style, self._styles['default'])

		self._kwargs = kwargs

	
	def __repr__(self) -> str:
		"""
		Shows information about the useful attributes of the object when printed
		Any attribute with length is only shown when length > 0
		The id is not shown
		"""
		return f"<Index section_names={repr(self._section_names)}, section_names=[{', '.join(self._section_names.values())}], bleeding={self._bleeding}, sep={repr(self._sep)}, style={repr(self._style)}>"

	def __call__(self, section_name: str, *args: Any, body: Optional['Body'] = None, bleeding: float=None, numbered: bool=True, transforms: List[Union[Callable, str, None]]=None, **kwargs: Any) -> str:
		_kwargs = self._kwargs.copy()
		_kwargs.update(kwargs)

		if (transforms is None):
			transforms = list()

		if (body is not None):
			transforms.append(body.__add__)

		if (numbered):
			self._section[-1] += 1

		entry = IndexEntry(
			self,
			section_name,
			_kwargs.get(DEFAULT_REFERENCE_KEY, section_name),
			*args, 
			section=numbered and self._section.copy(),
			transforms=transforms,
			bleeding=bleeding,
			**kwargs
		)

		return entry

	def __enter__(self, *args, **kwargs) -> Self:
		self._section[-1] -= 1
		self._section.append(1)
		return self

	def __exit__(self, *args, **kwargs):
		self._section.pop(-1)

	def place(self) -> DelayedIndex:
		return DelayedIndex(self)

	async def setup(self, output_path, output_fname, doc: 'Document') -> None:
		self._is_plugin_setup = True	

	async def clear(self) -> None:
		self._section_names.clear()
		self._section.clear()
		self._section.append(0)

	async def render(self, document: 'document', mode: str | int=None):
		"""
		"""
		pass
