from typing import *
import os

import pandas as pd
import plotly.express as px


from Lang.document import Document
from Lang.sections.abstract import abstract

from Lang.sections.title import title
from Lang.style.new_page import new_page
from Lang.html.table import table

from Lang.formulas.var import Var
from Lang.formulas.formula import Formula
from Lang.formulas.code import Code	

from Lang.markdown_text.markdown_text import markdown_text

from Lang.sections.index import Index
from Lang.citations.base_citations import Citations
from Lang.acronyms.with_cite.acronyms_with_cite import AcronymsWithCite
from Lang.glossary.wikipedia_glossary import WikipediaGlossary
from Lang.media.images import Images

# We create an index manager
index = Index()

# We create a glossary manager.
# This one takes from wikipedia the description of non-provided entries
# Every reload is quite slow, so disable it during the development
glossary = WikipediaGlossary()
python_gl = glossary.add('Python (programming language)', '[Disabled due to Wikipedia\'s overhead]')
pyarticles_gl = glossary.add(
	'PyArticles',
	"""
	PyArticles is A LaTeX alternative that uses Python classes to output a HTML + CSS file that can be printed
	"""
)

# We create a citations manager
bib = Citations()

# We create an acronyms manager.
# This one will automatically cite any citation that exists
# in the bibliography with the specified id
acro = AcronymsWithCite(citations=bib)
python = acro.add('Python', python_gl)

imgs = Images()

e = Var('e', 2.718)
softmax = Formula(1 / (1 + e ** (-Var('x'))))

tokens = {
	'-python': python,
	'-python_description': python_gl.description,
	'-pyarticles': pyarticles_gl,
	'-pyarticles_description': pyarticles_gl.description,
	'-softmax': softmax.render(),
	'-nl': "\n\n",
}

doc_plugins = [
	index,
	glossary,
	bib,
	acro,
	imgs,
]

# Try to change 'en' to 'es'
lang = 'en'
doc = Document(lang=lang, replacements=tokens, plugins=doc_plugins)

if(lang == 'es'):
	doc._lang_data.update({
		"Code": "Código",
		"Formulas": "Formulas",
		"Pandas_table": "Tabla de Pandas",
		"Plotly_image": "Imagen de Plotly",
		"Imported_lorem_ipsum": "Lorem ipsum importado",
	})
elif(lang == 'en'):
	doc._lang_data.update({
		"Code": "Code",
		"Formulas": "Formulas",
		"Pandas_table": "Pandas table",
		"Plotly_image": "Plotly image",
		"Imported_lorem_ipsum": "Imported lorem ipsum",
	})

@doc.attach
async def generate(document: Document) -> Document:
	body = document.body

	### TITLE

	# Replace with your title and subtitle.
	# Optionally, document.keywords can be used 
	# and the keywords will be in the specified language
	body += title(
		document.keywords.TITLE, 
		document.keywords.SUBTITLE,
		f'{document.keywords.AUTHOR}\n\nemail@example.com'
	)

	### ABSTRACT
	body += abstract(
		"""
		This is a template project for the creation of a -pyarticles article.
		-nl-nl
		-pyarticles_description.
		-nl-nl
		It is based on -python.
		-nl-nl
		-python_description
		""",
	)

	### INDEX
	body += index.place()
	body += new_page()

	### Introduction
	body += index(document.keywords.INTRODUCTION).render()

	# We can insert images without the need to download them
	body += imgs.add(
		'https://www.python.org/static/img/python-logo.png',
		caption="-python logo stolen from python.org",
	)\
	.render(document)\
	.float('right')

	body += """
	-python without citation (because it is the second apparition), as it appeared before
	in the abstract, and it had an explicit citation there.
	""",

	### Code
	body += index(document.keywords.Code)\
	.render()\
	.clear()\

	body += "We can decorate any function an it will be converted to a text representation of it"

	@Code
	def summarize_users(ages: List[int], min_age: int) -> Dict[str, Union[int, float, None]]:
		"""
		Summarizes user information by calculating the average age of users.
		"""
		total_age = 0
		num_users = 0
		
		for age in ages:
			if(age >= min_age):
				total_age += age
				num_users += 1
		
		average_age = total_age / num_users if num_users > 0 else None
		
		return {
			'num_users': num_users,
			'average_age': average_age
		}
	
	body += summarize_users.render()

	body += f"-nlExample 1: summarize_users([1, 2, 3, 4, 5, 6], 3): {summarize_users([1, 2, 3, 4, 5, 6], 3)}"
	body += f"-nlExample 2: summarize_users([1, 2, 3, 4, 5, 6], 7): {summarize_users([1, 2, 3, 4, 5, 6], 7)}"

	### Formulas
	with index(document.keywords.Formulas, body=body) as formulas_index:
		formulas_index += "We can also use formulas in the documentument, and to compute them-nl"

		# We can show the formula
		formulas_index += ["Softmax: ", softmax.render()]
		# And we can generate results if all variables are specified
		formulas_index += f"-nl-nlExample 1: softmax(4): {softmax.compute(x=4)}"
		formulas_index += f"-nlExample 2: softmax(4, e=2): {softmax.compute(x=4, e=2)}"

	### Tables
	body += index(document.keywords.Pandas_table).render()\
	.clear()

	body += "We can easily generate a table from a dataframe, no need of looking up the syntax on how to make a table"

	# Load data I randomly got online
	data = pd.read_csv(os.path.join(document.path, 'data.csv'), sep=';')
	data.Total = data.Total.replace({'.': 0, '..': 0}).astype(float)

	# We can quickly generate tables from a regular pandas-like dataframe
	body += table.from_pandas(data.drop_duplicates(subset=["Ramas de actividad"]))\
	.clear()

	### Images
	body += index(document.keywords.Plotly_image).render()

	body += "We also generate an image from a plotly Figure, no need of exporting or learning tikz"

	# We can quickly generate images from plotly images
	body += imgs.from_plotly(px.scatter(data, y="Total"), caption="Plotted the table's Total columns")\
	.render(document)\
	.float('center')

	### Markdown
	body += index("Markdown").render()\
	.clear()

	body += """
	-nl
	We can also use markdown in the documentument, and to generate it
	-nl
	"""

	body += markdown_text("""
	> _"Markdown allows you to express ideas clearly and beautifully!"_  
	> — **John Doe**

	---

	### Code Blocks & Syntax Highlighting

	You can include inline code like `const x = 10;`, or full code blocks:

	```javascript
	// JavaScript example:
	function greet(name) {
		return 'Hello, ${name}!';
	}

	console.log(greet("Markdown"));
	```
	""")

	### Importing
	body += document.import_part('sections/imported_lorem_ipsum.py', index=index)
