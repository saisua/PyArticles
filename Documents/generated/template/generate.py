import os

from Lang.document import Document

from Lang.sections.title import title
from Lang.style.new_page import new_page
from Lang.text.text import text
from Lang.html.span import span
from Lang.html.h import h

from Lang.sections.index import Index
from Lang.citations.base_citations import Citations
from Lang.acronyms.with_cite.acronyms_with_cite import AcronymsWithCite
from Lang.glossary.wikipedia_glossary import WikipediaGlossary
from Lang.media.images import Images

index = Index()

glossary = WikipediaGlossary()
python_gl = glossary.add('Python (programming language)')
pyarticles_gl = glossary.add(
	'PyArticles',
	"""
	PyArticles is A LaTeX alternative that uses Python classes to output a HTML + CSS file that can be printed
	"""
)

bib = Citations()

acro = AcronymsWithCite(citations=bib)
python = acro.add('Python', python_gl)

imgs = Images()

tokens = {
	'\python': python,
	'\python_description': python_gl.description,
	'\pyarticles': pyarticles_gl.name,
	'\pyarticles_description': pyarticles_gl,
}

async def generate(output_path: str, output_fname: str):
	if(not bib.loaded):
		# Bibliography will only be loaded once
		await bib.load_bibliography(os.path.join(output_path, 'bibliography.bib'))
	else:
		index.clear()
		acro.clear()
		bib.clear()
		imgs.clear()
	
	# Only 'en' and 'es' supported at the moment
	doc = Document(output_path, lang='en')

	body = doc.body
	body += title(
		doc.keywords.TITLE,
		doc.keywords.SUBTITLE,
		'Author\n\nemail@example.com'
	)

	body += h(2, doc.keywords.ABSTRACT)\
	.center()

	body += text(
		"""
		This is a template project for the creation of a \pyarticles article.
		\n
		\pyarticles_description\n
		\n
		It is based on \python.\n
		\python_description
		""",
		replacements=tokens
	)\
	.margin_left('15%').margin_right('15%')\
	.align('justify')
	body += new_page()

	body += index.render(doc)
	body += new_page()

	introduction = index('Introduction')
	body += introduction

	body += imgs.add(
		'https://www.python.org/static/img/python-logo.png',
		caption="Python logo stolen from python.org"
	)\
	.float('right')

	body += """
	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque mollis dictum blandit.
	Quisque tincidunt dapibus metus, sit amet aliquet odio dapibus vel.
	Donec pulvinar tincidunt nulla sed placerat. Pellentesque vel fringilla nisl. Nulla quis augue elit.
	Integer viverra enim ut mi cursus, non pulvinar mauris condimentum. Fusce in cursus tortor.\n
	\n
	Morbi non risus a arcu ullamcorper mollis eu nec ex. Vivamus consectetur turpis nisl.
	Duis in sem ut massa blandit dapibus. Nam et tortor nulla. Cras ac sodales lectus.
	Aenean aliquet, quam nec ullamcorper ornare, dui tellus feugiat risus, sit amet condimentum est mi sit amet eros.
	Sed in nunc eget ante imperdiet tempor at ut ligula. Sed eu sagittis mi, sit amet scelerisque justo.
	Sed tellus arcu, aliquet quis erat a, placerat varius risus. Aliquam in magna vel dolor interdum scelerisque.
	Donec ex diam, dapibus id consectetur a, lobortis eget tellus. Praesent scelerisque tincidunt ligula, sit amet semper tellus placerat a.\n
	\n
	Pellentesque eu mauris in sem commodo pharetra a vitae diam. In tristique lectus ut dolor sollicitudin convallis.
	Mauris eu augue congue, aliquet mi at, ullamcorper metus. In sed convallis mi.
	Fusce sollicitudin sodales felis, ut convallis nibh iaculis a. Aenean volutpat malesuada auctor.
	Suspendisse hendrerit nulla ligula, vitae hendrerit nibh semper sit amet. Aenean fringilla ornare fringilla.
	Etiam in est tristique est lobortis vehicula. Vestibulum finibus porta dui.
	Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.
	Integer a nulla sed tortor elementum vehicula. Nulla tempor lorem arcu, non scelerisque arcu mattis ac. Morbi quis egestas ex.\n
	\n
	Duis facilisis hendrerit iaculis. Vivamus metus nulla, faucibus sit amet mattis sit amet, eleifend non massa.
	Vestibulum lectus urna, aliquet vel magna eget, porttitor euismod turpis. Fusce eget sem ac massa dictum lacinia id vel leo.
	Donec eget posuere dolor. Fusce fringilla sapien sed metus porta finibus. Etiam a ex vitae felis tempus sollicitudin sodales vel elit.
	Nulla facilisi. Pellentesque consequat enim at nulla mollis viverra.\n
	\n
	Etiam posuere nibh dui, in convallis elit eleifend id. Sed orci purus, blandit eget nisi quis, congue suscipit libero. Nulla facilisi.
	Duis at scelerisque metus, feugiat consequat ligula. Sed eget ultricies arcu, et aliquet diam.
	Aliquam porttitor neque enim, eu viverra purus tempus et. Suspendisse in gravida ligula, a aliquet lacus.
	"""

	body += imgs.render(doc)
	body += acro.render(doc)
	body += glossary.render(doc)
	body += bib.render(doc)
			  
	await doc.store(output_path, output_fname)
