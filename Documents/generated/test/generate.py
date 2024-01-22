import os

from Lang.document import Document

from Lang.sections.index import Index
from Lang.citations.base_citations import Citations

from Lang.sections.title import title
from Lang.text.text import text
from Lang.html.h import h
from Lang.html.a import a

from Lang.media.image import image

from Lang.html.table import table

from Lang.style.new_page import new_page

from Lang.formulas.formula import formula
from Lang.formulas.var import Var

from Lang.acronyms.with_cite.acronyms_with_cite import AcronymsWithCite
from Lang.glossary.wikipedia_glossary import WikipediaGlossary

glossary = WikipediaGlossary()
rl_gl = glossary.add('Reinforcement Learning')

bib = Citations()

acro = AcronymsWithCite(citations=bib)
rl = acro.add(
	'RL', 
	rl_gl,
	short_plural='RLs',
	long_plural='Reinforcement Learnings'
)

vardiv = abs(Var('test') / 3)

async def generate(output_path: str, output_fname: str):
	if(not bib.loaded):
		await bib.load_bibliography(os.path.join(output_path, 'bibliography.bib'))
	else:
		acro.clear()
		bib.clear()
	
	sect = Index()
	doc = Document(output_path)

	body = doc.body
	body += title(
		'test title',
		'test subtitle',
		'Autheur',
	)

	body += h(2, text("Abstract"))\
	.center()
	body += text(rl_gl.description)\
	.margin_left('15%').margin_right('15%')\
	.align('justify')
	body += new_page()

	body += sect.index
	body += new_page()

	introduction = sect('Introduction', id='introduction')
	body += introduction
	body += image('https://1.bp.blogspot.com/-v41GxYnmUbs/XqGdGlGz9VI/AAAAAAAAAWw/Bt5zqsRskj4HT3Z5rzrSURLHsKgTu6fgQCK4BGAsYHg/py.png')\
	.resize(width='10%')\
	.float('right')
	body += rl

	body += formula(vardiv) + text(f' = {vardiv.compute(test=-15)}')

	with sect:
		section = sect('Context')

		section += (
			text("Low effort lorem ipusum "),
			text("Test"),
			bib.cite('RL', '\n'),
			text("Low effort lorem ipusum 2\n")
			+
			text("low effort 3")
			+
			bib.cite('RL', '\n\n')
			+
			a(text("Goto intro"), href=introduction)
		)

		body += section


	body += table(
		[['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h']],
		header=['A', 'B', 'C']
	)
	# body += wikipedia_image('Tiger', image_index=1)\
	# .resize(width='30%')\
	# .float('center')

	body += new_page()
	body += sect("Lorem Ipsum")\
	.clear('both')

	body += text("""
	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vitae orci vulputate risus fringilla facilisis sit amet eget arcu. Ut id tellus dapibus, placerat ex et, egestas risus. Curabitur tristique quis ante id gravida. Proin nec dictum magna, vitae vulputate ipsum. Vestibulum arcu diam, congue semper tortor sit amet, semper viverra erat. Mauris elementum dolor vel nisl porta ultricies. Etiam dignissim odio vel congue volutpat. In nisl lectus, tempus vel tortor id, scelerisque gravida libero. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Praesent dapibus, odio quis finibus blandit, ex ante pulvinar sem, vel mollis massa arcu nec elit. Sed in egestas urna. Pellentesque condimentum velit quis neque egestas facilisis. Mauris at nisl pharetra, efficitur nulla dictum, egestas sem. Ut odio leo, cursus ut scelerisque quis, scelerisque in mi. Integer euismod lectus ac metus euismod eleifend. Fusce non porttitor mauris.

	Mauris sit amet gravida nisl. In quis pellentesque leo. Vivamus ultricies tellus tortor, sed vehicula diam rutrum ac. Mauris vehicula est at neque posuere accumsan. Nullam vel eros ac ligula tincidunt condimentum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aliquam ut orci nec tortor volutpat lobortis. Aenean massa enim, consectetur non elementum quis, dictum at massa. Integer tincidunt ornare sem, eu rhoncus dolor aliquet in. In hac habitasse platea dictumst. Quisque gravida velit quis risus posuere, et pulvinar urna convallis. Duis aliquet viverra libero a tristique. Donec tempus non mauris vitae egestas. Integer vel velit consequat, vulputate mi sit amet, auctor lorem.

	Sed dictum tristique turpis, mollis venenatis dui vulputate sed. Vivamus eros neque, sodales vel mi in, varius placerat tortor. Sed vitae ante tellus. Integer quis ipsum magna. Pellentesque elementum magna ante, id lacinia ex pharetra aliquam. Morbi a eleifend elit. Quisque non pellentesque erat. Cras sit amet nunc nulla.

	Praesent sit amet nisi pulvinar, posuere massa a, faucibus urna. Etiam ullamcorper urna dolor, quis placerat turpis bibendum id. Sed vitae finibus nisl. Nam venenatis metus vel arcu tristique, commodo feugiat tortor ornare. Praesent vitae arcu orci. Donec quis egestas arcu. Donec interdum lorem eu tristique accumsan. Proin volutpat ligula eros, eget mattis sem aliquet sed. Mauris fermentum posuere velit, sed mollis urna ornare et. Donec quis facilisis odio. Nullam ornare nibh sed urna porttitor vestibulum. Duis pharetra enim nisl, sit amet imperdiet nibh efficitur eu. Ut sit amet nulla mauris. Morbi semper convallis sodales. Aenean cursus vulputate dui, quis rutrum lectus ultrices ac. Fusce ut arcu tortor.

	Aliquam erat volutpat. Nulla dapibus mi a felis convallis sodales. Vivamus massa turpis, tincidunt non vehicula eu, malesuada nec tortor. Etiam dignissim efficitur odio in imperdiet. Suspendisse ut auctor leo, ut imperdiet nulla. Aenean vestibulum arcu vel arcu imperdiet convallis. Fusce dictum ipsum non ultrices ullamcorper. Mauris ac sollicitudin mi. Fusce ornare augue quis neque efficitur, sit amet imperdiet nisl facilisis. Etiam pellentesque sit amet velit vitae scelerisque. Nam tempus dui tortor, sed laoreet ante placerat vitae. Praesent id luctus est, a placerat dui. Quisque mauris ex, semper et eros a, vestibulum cursus tellus. Sed enim enim, faucibus vitae iaculis eleifend, eleifend vitae turpis. Maecenas vehicula metus molestie odio porta blandit. In hac habitasse platea dictumst.

	Sed luctus finibus sem, eget vehicula nisl eleifend imperdiet. Nulla facilisi. Cras justo magna, volutpat et enim semper, dapibus dignissim erat. Duis quis rhoncus urna. Aliquam et pellentesque mi. Donec hendrerit elementum eleifend. Proin non ante rutrum, sollicitudin justo quis, lobortis est. Aliquam erat volutpat. Nulla sed nulla ut lacus accumsan gravida. Nam pretium condimentum leo, id egestas velit tristique at. Aenean at consequat arcu.

	Suspendisse in gravida nunc. Pellentesque ac pulvinar nunc. Suspendisse augue tortor, placerat ut diam non, vehicula finibus massa. Aliquam id orci lacinia, hendrerit ante dignissim, pulvinar sapien. Vestibulum fermentum tincidunt lobortis. Donec nec lectus ex. Duis eget est fringilla, maximus odio pellentesque, dictum quam. Nulla hendrerit ullamcorper consequat. Curabitur vel nunc facilisis, volutpat sem nec, placerat arcu. Morbi tempus varius volutpat. Cras varius, sapien vitae tincidunt ultricies, quam velit porttitor sapien, id pharetra sem tortor varius erat.

	Praesent tempor, nulla vitae pellentesque pretium, magna erat feugiat nibh, eget hendrerit nulla orci vel libero. In hendrerit eu ante vitae congue. Sed et mauris feugiat, consectetur metus eu, venenatis ex. Vivamus sagittis eros quis dapibus scelerisque. Fusce ut fringilla neque. Duis efficitur eros neque, ac luctus erat rhoncus sed. Fusce pretium dignissim est, ut ultrices eros commodo quis. Ut vitae dui a nulla venenatis sodales. Praesent et lacinia purus. Praesent tempor massa ac maximus dapibus. Aliquam a volutpat sem. Maecenas neque elit, mattis eget tortor nec, consectetur luctus ex.

	Fusce sit amet augue a odio feugiat euismod aliquet a mi. Nam pellentesque ex ligula, ut rutrum est tempus a. Nulla nec odio placerat, pellentesque dolor eu, laoreet ligula. Morbi ac pretium lectus. Ut tempus lorem in congue vulputate. Proin condimentum iaculis enim. Etiam interdum risus eu neque porttitor ultricies. Sed nec sapien non libero ornare semper. Nulla facilisi. Proin bibendum finibus arcu, quis ullamcorper neque pharetra a. Nullam sed arcu sed sem posuere egestas. Aenean sodales mi sed maximus lobortis.

	Aenean congue dui urna, non tristique enim sollicitudin eget. Cras in augue mattis, fermentum ante at, euismod metus. Maecenas id iaculis orci. Sed vel feugiat augue. Vivamus tempor neque quam, in egestas justo posuere vel. Sed et tempor ipsum, in laoreet mauris. Integer luctus arcu et ex blandit ullamcorper. Vivamus lacus neque, congue vel suscipit at, accumsan eu tortor. Sed blandit ultrices est. Suspendisse in enim vel eros dapibus tempus sit amet id lectus. Nunc at aliquet est. Nunc erat massa, tincidunt eu risus nec, varius ullamcorper purus. Sed sed mattis metus. Integer condimentum odio ut neque laoreet, vitae porta diam consectetur.

	Suspendisse finibus eleifend suscipit. Cras non consectetur tortor. Sed volutpat lacus vel lacinia scelerisque. Etiam et porttitor lectus. Fusce vel interdum lacus. Nulla pellentesque elementum orci quis euismod. Praesent ante neque, varius vitae tellus sed, ultrices placerat lectus. Sed tincidunt ullamcorper elit, quis pharetra libero aliquam eget. Pellentesque eleifend ante dui, at mollis orci vulputate sit amet. Vivamus risus massa, tincidunt nec risus ac, iaculis fringilla arcu. Ut semper odio quam, at accumsan quam consequat non. Curabitur non bibendum lorem. Duis id dapibus neque. Mauris porta euismod tortor sit amet dictum.

	Suspendisse potenti. Donec ut viverra leo, ac eleifend ex. Vivamus ut ornare nunc, a egestas nunc. Integer blandit, lorem eget eleifend porttitor, eros nulla tristique neque, a dictum leo lorem sed nisl. Morbi mollis vehicula odio, a sagittis augue congue rutrum. Fusce rhoncus consectetur diam, in blandit nunc dignissim sed. Praesent et gravida magna. Vivamus mattis arcu ac scelerisque volutpat.

	Maecenas laoreet efficitur turpis, eget egestas quam pulvinar in. Mauris tempus scelerisque varius. Sed hendrerit rhoncus facilisis. Nunc malesuada eu risus quis mollis. Quisque rutrum est vitae felis vestibulum, non volutpat nunc auctor. Integer in hendrerit felis. Ut ultrices odio quis iaculis maximus. Nam eget mi eu ex semper vulputate. Ut quis ante odio. Mauris ornare justo eget massa auctor, non cursus arcu tincidunt. Nunc eu dictum mauris. Nullam risus purus, congue eget finibus nec, faucibus sit amet tortor.

	Sed velit justo, suscipit eget neque sit amet, placerat fermentum sem. Maecenas dictum ligula neque, sed congue risus placerat id. In semper tortor eget euismod cursus. Duis efficitur elit ante, ac ullamcorper ante fringilla eget. Proin urna elit, vulputate id malesuada vitae, commodo ut enim. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Vestibulum vitae risus nec orci posuere pellentesque ac eu nisl. Praesent vitae ligula nec dolor ornare varius ac eget mauris. Donec non faucibus nibh. Donec a turpis egestas, varius justo vitae, faucibus ex. Etiam ut elit magna. Etiam dolor ligula, vestibulum vel arcu quis, lobortis suscipit nulla. Maecenas metus sem, facilisis nec nulla ut, ultrices rutrum neque. Phasellus faucibus lectus eu ligula vulputate iaculis.

	Nulla elementum nulla risus, eu vulputate dui congue at. Aenean vitae lorem in lorem efficitur tempor. Ut finibus, libero vitae consectetur convallis, arcu libero luctus sapien, nec ullamcorper eros magna in augue. Nam efficitur at sem sit amet imperdiet. Nunc vel sagittis lectus, quis cursus purus. Curabitur quis metus in ipsum dictum molestie. Praesent in arcu imperdiet, finibus purus vitae, volutpat mi. Pellentesque rhoncus congue diam, sit amet condimentum leo. Pellentesque et lacus sit amet nunc bibendum efficitur et non lectus. Curabitur ultrices ullamcorper risus, a faucibus ligula.

	Aenean hendrerit sed enim eu auctor. Phasellus tincidunt metus eu mi elementum ultrices. Proin libero nunc, bibendum ut elit a, ultrices ullamcorper nisl. Ut ullamcorper tincidunt quam, aliquet pharetra quam faucibus nec. Phasellus dictum rhoncus tortor, eu sodales nisi rhoncus at. Donec eu urna nec sem fermentum pulvinar ut eget ligula. Nulla imperdiet ut velit vitae mollis. Aliquam sit amet placerat turpis. Nullam sem justo, facilisis sed tempor et, pellentesque sed leo. Pellentesque congue cursus erat, nec blandit turpis cursus eu.

	Fusce laoreet eget ligula ac iaculis. Aenean consequat nisl vel dolor congue placerat. Nunc elementum ac eros et mollis. Cras accumsan ligula quis dolor bibendum molestie. Donec scelerisque iaculis ante nec blandit. Quisque at scelerisque purus, vitae molestie sapien. Maecenas rhoncus ex id congue aliquet. Proin id orci orci. Donec est enim, varius et volutpat vitae, malesuada eget nulla. Etiam lorem ante, finibus sit amet neque sit amet, tempus maximus mauris. Curabitur fermentum magna eu odio vestibulum tempor. Vivamus sed elit porttitor, faucibus tellus volutpat, sodales lorem.

	In auctor enim eu massa pharetra, at porttitor magna volutpat. Donec rutrum convallis tempor. Maecenas lorem nibh, tincidunt et bibendum non, vulputate vel elit. Integer at magna ullamcorper turpis venenatis congue in non nisl. Nam sagittis tincidunt tortor, non dignissim magna consequat ac. Phasellus porttitor pulvinar eleifend. In tristique, ex in varius dignissim, lacus quam faucibus ligula, ut consectetur est elit at augue. Maecenas at gravida ipsum. Vestibulum vitae metus id elit mattis blandit.

	In ullamcorper auctor massa, sed ornare est commodo in. Fusce ut porta arcu, ut pretium sapien. Nunc eros erat, fringilla at lobortis sit amet, fermentum sed dui. Nunc ullamcorper, dui id suscipit lacinia, libero ipsum consectetur lorem, pulvinar ultrices orci dui sit amet lorem. Vestibulum imperdiet sit amet metus quis convallis. Vestibulum cursus sagittis sapien, porttitor luctus dui. Praesent vehicula erat in suscipit euismod. In tempus hendrerit tellus non lacinia. Suspendisse potenti. Cras ut velit purus. Pellentesque diam arcu, malesuada ac euismod ut, sollicitudin id arcu. In hac habitasse platea dictumst. Nam eget facilisis turpis. Cras et justo nec lacus facilisis ornare vel non enim. Proin at felis vel nisl finibus efficitur. Cras malesuada, lorem sed laoreet iaculis, lacus sem elementum neque, tempus vestibulum massa ipsum sed neque.

	Vestibulum volutpat eleifend dolor eget aliquam. Curabitur sed est ante. Donec non orci semper, lacinia mi sed, luctus ligula. Ut non sem hendrerit, porttitor ante sed, interdum tortor. Phasellus lacinia faucibus erat, nec suscipit elit egestas nec. Cras egestas diam quis justo facilisis consequat. Etiam sit amet quam id ante pellentesque lacinia. Curabitur eleifend leo et rhoncus sodales. Fusce dignissim dui augue, non tincidunt arcu finibus nec. Morbi a risus ipsum. 
	Rerum ad velit et. Temporibus repellat distinctio error vitae nostrum voluptas consectetur delectus. Ut temporibus sapiente quos hic. Et at eveniet provident qui velit similique. Ut aut sit et exercitationem sunt. Non corporis illo quis consequuntur est.
	Totam commodi vero voluptates. Possimus quis excepturi sit qui. Qui a id autem quidem earum. Necessitatibus sit unde inventore dolor. Qui consequuntur ea earum molestiae magni cumque ut.
	Est ullam possimus dolorum. Eum iusto et minus quasi recusandae impedit. Omnis in maxime dolor perferendis qui est unde sequi. Esse sint inventore voluptatem sed eligendi quis et.
	Laudantium tempora laudantium veritatis. Ab odit consequatur maxime. Porro molestiae quibusdam laboriosam impedit doloremque non. Suscipit consectetur quo voluptates voluptates consequatur. Quo sed sunt est ut nemo odio totam.
	Quia ut sed voluptates voluptatibus inventore iusto. Maiores in recusandae voluptatem in aspernatur iure. Quia voluptatem veritatis aspernatur laborum ea. Nostrum perspiciatis sed enim sed. Dolorem adipisci odit veritatis amet fugit mollitia.
	
	""").align('justify')

	body += acro.render()
	body += glossary.render()
	body += bib.render()
			  
	await doc.store(output_path, output_fname)