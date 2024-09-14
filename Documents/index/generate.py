import os

from Lang.document import Document

from Lang.text.text import text

from Lang.html.h import h
from Lang.html.a import a
from Lang.lists.unordered import unordered_list

doc = Document()

@doc.attach
async def generate(doc: Document):
	body = doc.body
	body += h(1, "Documents")

	body += unordered_list([
		a(f"{doc_name}/", href=f"/{doc_name}")
		for doc_name in os.listdir('Documents/generated')
	])
