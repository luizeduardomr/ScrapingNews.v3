from src.browser import *
import time
import re

clear = lambda x : re.sub('\s+', ' ', x.text.replace('\n', ' '))

with open(os.path.join('src', 'main.js')) as infile:
	elimn_assin = infile.read()


def search(query, DIAi, MESi, ANOi, DIAf, MESf, ANOf):
	br = GLOBAL_BR
	query = query.replace(' ', '%20')
	### Realiza a busca
	#br.get('https://busca.uol.com.br/result.html?term={0}#gsc.tab=0&gsc.q={0}%20site%3Anoticias.uol.com.br'.format(query.replace(' ', '%20')))

	#YYYY-MM-DD

	br.get(f'https://busca.uol.com.br/result.html?term={query}+site%3Anoticias.uol.com.br#gsc.tab=0&gsc.q={query}%20site%3Anoticias.uol.com.br%20after%3A{ANOi}-{MESi}-{DIAi}%20%20before%3A{ANOf}-{MESf}-{DIAf}')
	br.execute_script(elimn_assin)

	try:
		secaoqntd = WAIT_TXT(
			'/html/body/div[2]/section[2]/div/div/div/div/div/div[3]/table/tbody/tr/td/div')
		valor = int(secaoqntd.split(' ')[1])
		print(valor)
	except:
			print_exc()
	data = []
 
	i = 0
	c = 0
	p = 1

	try:
		GET('/html/body/div/div[1]/div[1]/a')
		d = 1
	except:
		d = 2

	while c < valor:
		i+=1
		c+=1

		## Tenta pegar a proxima noticia
		time.sleep(.5)
		try:
			el = WAIT_GET(f'/html/body/div[2]/section[2]/div/div/div/div/div/div[5]/div[2]/div/div/div[{d}]/div[{i}]/div[1]')
		except:
			## Se nao tiver, tenta avancar para a proxima pagina
			p += 1
			try:
				CLICK(f'/html/body/div[2]/section[2]/div/div/div/div/div/div[5]/div[2]/div/div/div[3]/div/div[{p}]')
				i = 0
				continue
			except:## Nao tem pagina seguinte, eh so uma pagina de resultados
				break

		## Pega as informacoes do headline da noticia
		hdr =  GET(f'/html/body/div[2]/section[2]/div/div/div/div/div/div[5]/div[2]/div/div/div[{d}]/div[{i}]/div[1]/div[1]/div/a')
		link = hdr.get_attribute('href')
		title = hdr.text

		splits = link.split('/')
		try:
			year   = [x for x in splits if x.startswith('20')][0]
		except:
			c -= 1
			continue

		month  = splits[splits.index(year)+1]
		day    = splits[splits.index(year)+2]

		descr = TXT(f'/html/body/div[2]/section[2]/div/div/div/div/div/div[5]/div[2]/div/div/div[{d}]/div[{i}]/div[1]/div[3]/div/div[2]')
		descr = descr.split('...')[1].strip() + '...'

		## Cria o objeto da noticia no json
		data.append({
				'link'  : link,
				'title' : title,
				'descr' : descr,
				'date'  : f'{day}/{month}/{year}'
			}
		)


	## Para cada notica, abre o artigo e puxa o conteudo
	for i in range(len(data)):
		link = data[i]['link']
		br.get(link)
		time.sleep(.5)

		try:
			content = WAIT_TXT('/html/body/div[8]/article/div[2]/div/div[1]/div/div[2]/div[1]/div[3]')
			print(f'Conteúdo da linha 95:\n {content}\n\n')
		except:
			try:
				content = WAIT_TXT('/html/body/article/div[2]/div/div[1]/div/div[2]/div[1]/div[3]')
				print(f'Conteúdo da linha 99:\n {content}\n\n')
			except:
				try:
					content = WAIT_TXT('/html/body/article/div[2]/div/div[1]/div/div[3]/div[1]/div[3]')
					print(f'Conteúdo da linha 103:\n {content}\n\n')
				except:
					try:
						content = WAIT_TXT('/html/body/div[8]/article/div[3]/div/div[1]/div/div[2]/div[1]/div[3]/p')
						print(f'Conteúdo da linha 107:\n {content}\n\n')

					except:
						#GET('/html/body/div[7]/div/div[2]/div[1]/div/div[1]')
						content = "Apenas Video"
						pass
		data[i]['content'] = content

	return data, valor