from Lang.i18n.languages import all as languages_data

from Lang.compatibility import *

class traductions:
	_data: Dict[str, str]

	def __init__(self, lang: str='en') -> None:
		self._data = languages_data.get(lang, languages_data['en'])

	def __getitem__(self, item: str) -> str:
		return self._data[item]

	def items(self):
		return self._data.items()

	def values(self):
		return self._data.values()

	def keys(self):
		return self._data.keys()

	def update(self, data: Dict[str, str]):
		self._data.update(data)
