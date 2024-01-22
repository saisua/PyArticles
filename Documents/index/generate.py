import os

from Lang.document import Document

from Lang.text.text import text

from Lang.html.h import h
from Lang.html.a import a
from Lang.lists.unordered import unordered_list

async def generate(output_path: str, output_fname: str):
	doc = Document(output_path)

	body = doc.body
	body += h(1, text("Documents"))\

	body += unordered_list([
		a(text(f"{doc_name}/"), href=f"/{doc_name}")
		for doc_name in os.listdir('Documents/generated')
	])

	await doc.store(output_path, output_fname)