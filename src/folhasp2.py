from src.browser import *
import time
import re
import os
from selenium.webdriver.common.action_chains import ActionChains

with open(os.path.join('src', 'main.js')) as infile:
    elimn_assin = infile.read()

def clear(x): return re.sub('\s+', ' ', x.text.replace('\n', ' '))

# def clear2(x):
#     return x.find_element_by_tag_name('p')

def search(query, DIAi, MESi, ANOi, DIAf, MESf, ANOf):

    br = GLOBAL_BR  
    query = query.replace(' ', '+')
    # Realiza a busca

    # https://search.folha.uol.com.br/search?q=Mudanças+climáticas&periodo=personalizado&sd=05%2F04%2F2020&sd=&ed=03%2F08%2F2020&ed=&site=todos
    # br.get('https://search.folha.uol.com.br/?q={}&site=todos'.format(query.replace(' ', '+')))
    # br.get(f'https://search.folha.uol.com.br/search?q={query}&periodo=personalizado&sd={DIAi}%2F{MESi}%2F{ANOi}&sd=&e d={DIAf}%2F{MESf}%2F{ANOf}&ed=&site=jornal')
    #f'https://search.folha.uol.com.br/search?q={query}&periodo=mes&sd=&sd=&ed=&ed=&site=todos')
    # filtro por ano (personalizado é bugado de mais)

    br.get(f'https://search.folha.uol.com.br/search?q={query}&periodo=personalizado&sd={DIAi}%2F{MESi}%2F{ANOi}&ed={DIAf}%2F{MESf}%2F{ANOf}&site=todos')
    br.execute_script(elimn_assin)

    try:
        secaoqntd = TXT(
            '/html/body/main/div/div/form/div[2]/div/div/div[2]/div[2]/div[1]')
        valor = int(secaoqntd.split(' ')[0])
        print(valor)
    except:
        valor = 5

    data = []

    i = 0
    c = 0
    contador = 0
    vintecinco = 25

    time.sleep(5)

    # Clica para aceitar os Cookies (TEMPORÁRIO)
    if(findElement('/html/body/div[11]/div/div[2]/button') != 0):
        CLICK('/html/body/div[11]/div/div[2]/button')

    while c < valor:
        i += 1 #label da notícia
        c += 1
        
        br.execute_script("window.scrollTo(0, 1080)")
        # Verifica se está no fim da página
        if(i == 26):
            print('\n')
            # Verifica se ainda tem o botão para ir para a próxima página
            # Se tiver, ele clica. Senão, significa que acabaram as notícias
            if(findClass('c-pagination__arrow') != 0):
                br.find_elements_by_class_name('c-pagination__arrow')[-1].click()
                i = 0
                print(f'================= entrou no if l.62 --- Valor do i:  {i} ========================')
                continue
                time.sleep(.10)
            else:
                print('erro pra pular de página-------------------------------------')

        # Tenta pegar a proxima noticia
        try:
            if(findElement(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]') != 0):
                corpoglobal = WAIT_GET(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]')

            elif(findElement(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]') != 0):
                corpoglobal = WAIT_GET(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]')
                #corpoglobal = WAIT_GET(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]/div[2]/div/a')
        except:
            # Se nao tiver, tenta avancar para a proxima pagina
            if(findElement('/html/body/main/div/div/form/div[2]/div/div/div[2]/nav/ul/li[8]/a') != 0):
                CLICK('/html/body/main/div/div/form/div[2]/div/div/div[2]/nav/ul/li[8]/a')
            else:
                pass
            
        # Pega as informacoes do headline da noticia
        descr = corpoglobal.find_element_by_tag_name('p').text
        #print([x.text for x in corpoglobal.find_elements_by_tag_name('p')])
        link = corpoglobal.find_element_by_tag_name('a').get_attribute('href')
        title = clear(corpoglobal.find_element_by_class_name('c-headline__title'))
        date = corpoglobal.find_element_by_tag_name('time').get_attribute('datetime')
        secaoNoticia = corpoglobal.find_element_by_tag_name('h3').text
        #descr = clear(el.find_element_by_tag_name('p'))

        # Altera a ordem da data (12.nov.2019 às 13h01) 
            # [12] [nov] [2019 às 13h01]
        date = date.split('.')

        if any ([x in secaoNoticia for x in['FOTOFOLHA']]):
            c -= 1
            continue

        # Coleta a informação de Imagem
        if findElement(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]/div[2]/div/a/img') != 0:
            isImagemtxt = 'Tem imagem'
        else:
            isImagemtxt = 'Não tem imagem'

        print(f'{i} - {title}')

        if(' - ' in secaoNoticia):
            secaoNoticia = secaoNoticia.split(' - ')[1]
        data.append({
            'link': link,
            'title': title,
            'descr': descr,
            'date': date,
            'imagem': isImagemtxt,
            'secao': secaoNoticia
        }
        )
        #print(data[-1])

    # Para cada notica, abre o artigo e puxa o conteudo
    for i in range(len(data)):
        link = data[i]['link']
        br.get(link)
        lista = []
        try:
            content = wait(
                lambda: CLASS('c-news__body'),
                lambda: CLASS('js-news-content'),
                lambda: CLASS('c-news__content')
                )
            for paragrafo in content.find_elements_by_tag_name('p'):
                lista.append(paragrafo.text)
            content = "\n".join(lista)
        except:
            content = 'erro no conteúdo durante a coleta de dados'
        data[i]['content'] = content

    return data, valor