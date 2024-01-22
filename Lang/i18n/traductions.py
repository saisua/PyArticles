from typing import *

from Lang.i18n.languages import all as languages_data

class traductions:
	_data: Dict[str, str]

	def __init__(self, lang: str='en') -> None:
		self._data = languages_data.get(lang, languages_data['es'])

	def __getitem__(self, item: str) -> str:
		return self._data[item]