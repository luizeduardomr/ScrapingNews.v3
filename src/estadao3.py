from src.browser import *
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import traceback
import datetime

# with open(os.path.join('src', 'main.js')) as infile:
# 	elimn_assin = infile.read()

valores = {
       "totais" : 0,
       "coletadas" : 0,
       "ignoradas": 0
}

def search(query, DIAi, MESi, ANOi, DIAf, MESf, ANOf):
    querylink = tempo(query, DIAi, MESi, ANOi, DIAf, MESf, ANOf, quit=True)
    print(f'\n\nNotícias totais: {valores["totais"]}')
    print(f'Link da notícia original: {querylink}')
    inicio = datetime.datetime(*[int(x) for x in [ANOi, MESi, DIAi]]) 
    fim = datetime.datetime(*[int(x) for x in [ANOf, MESf, DIAf]])
    resultados = []
    valor = 0

    while(inicio<fim):
        temporaria = inicio + datetime.timedelta(days = 7)
        res, val =  tempo(query, inicio.day, inicio.month, inicio.year, temporaria.day, temporaria.month, temporaria.year, quit=False)
        resultados += res
        valor += val
        inicio = temporaria
        print('\n--------------------------------------')
        print(f'Notícias totais: {valores["totais"]}')
        print(f'Notícias coletadas: {valores["coletadas"]}')
        print(f'Notícias ignoradas: {valores["ignoradas"]}')
        print('--------------------------------------\n')
    return resultados, valor

def tempo(query, DIAi, MESi, ANOi, DIAf, MESf, ANOf, quit):
    br = GLOBAL_BR
    query = query.replace(' ', '+')
    # Realiza a busca
    br.get(f'https://acesso.estadao.com.br/login/?r=https://www.estadao.com.br/')
    time.sleep(2)

    # Entrar com a conta
    try:
        GET(f'/html/body/section/div/section/div[1]/form[1]/div[4]/div/div/input').send_keys('isabellagobbi@hotmail.com')
        GET(f'/html/body/section/div/section/div[1]/form[1]/div[5]/div/div/input').send_keys('Mudançaclimática20')
        time.sleep(2)
        try:
            CLASS('btn-azul').click()
        except:
            print_exc()
    except:
        pass

    time.sleep(2)

    # Realiza a busca
    querylink = f'https://busca.estadao.com.br/?tipo_conteudo=&quando={DIAi}%2F{MESi}%2F{ANOi}-{DIAf}%2F{MESf}%2F{ANOf}&q={query}'
    br.get(querylink)

    # Pega a quantidade de resultados da pesquisa
    try:
        secaoqntd = TXT('/html/body/section[3]/div/section/form/section/div/p')
        valor = int(secaoqntd.split(' ')[2])
    except:
        valor = 1

    if quit:
      valores["totais"] = valor
      return querylink

    calculopage = int(valor/10) + (valor%10 != 0)

    #print(f'Notícias encontradas (7 dias): {valor}')

    # Clica em ACEITAR as politicas de cookies  
    time.sleep(4)
    try:
        CLICK('/html/body/div[6]/div/div/div[2]/button') 
    except:
        try:
            CLICK('/html/body/div[6]/div/div[2]/button')
        except:
            pass

    time.sleep(5)
    # Tenta ja expandir a primeira vez os resultados - O primeiro botao de "carregar mais" se comporta diferente dos demais
    br.execute_script("window.scrollTo(0, 1080)")

    # Clica para fechar o anúncio
    try:
        CLICK('/html/body/section[5]/div/div/button')
    except:
        try:
            GET('/html/body/section[5]/div/div/button').click()
        except:
            print('não clicou para fechar o anuncio ----------------------------')
            pass

    # Clica no primeiro botão que é diferente dos demais
    try:
        CLICK('/html/body/section[4]/div/section[1]/div/section[2]/div/a')
    except:
        try:
            GET('/html/body/section[4]/div/section[1]/div/section[2]/div/a').click()
        except:
                try:
                    CLASS('go more-list-news btn-mais fn brd-e').click()
                except:
                    #print('erro no click do botão---------------------------------')
                    pass
                    print(querylink)
    time.sleep(3)
    data = []
    i = 0
    c = 0
    contador = 0
    isImagem = False
    # ==============================================================================================================================

    # Avanças as páginas até o final
    for page in range(2, calculopage):
        try:
            WAIT_CLICK('/html/body/section[4]/div/section[1]/{}section[11]/div/a'.format('div/' *page))
        except:
            print(f'Página atual: {page} -----------------------------------------------')
            print('/html/body/section[4]/div/section[1]/{}section[11]/div/a'.format('div/' *page))
            print(f'\n{querylink}\n')
            continue
    pagina = 1
    while c < valor:
        i += 1
        c += 1

        # Incrementar página e resetar 'i'     
        if(i==11 and pagina<=calculopage):
            i = 1
            pagina += 1
            valores["coletadas"] += 10


        # Tenta pegar um 'clicavel' novo
        try:
            corpo = WAIT_GET('/html/body/section[4]/div/section[1]/div/{}section[{}]'.format('div/' *pagina, i))
        except:
            # Se nao tiver, acabou todas as noticias ou deu erro :/
            print('\nerro para pegar o corpo da notícia')
            print_exc()
            print(querylink)
            break

        # Recebe todas as tags <a> para coletar o título, link e descrição
        corpo_tagA = corpo.find_elements_by_tag_name('a')

        # Entra na tag <a> de cada corpo da notícia (Onde contem a descrição e o título) ---------------------------------------------
        el = [x for x in corpo_tagA if len(x.text.strip())]
        if len(el) == 0:
            continue
        el = el[0]

        # Pega O link do headline da noticia
        link = el.get_attribute('href')

        # Filtro de conteúdo relevante
        if any(c in link for c in ('link.', 'tv.', 'paladar.', 'fim.', 'emais.', 'brpolitico.', 'einvestidor.', 'jornaldocarro.')):
            c -=1
            contador += 1
            print(f' Filtrou conteudo: {i}  --- qntd: {contador}')
            continue

        if 'estadao' not in link:
            c -= 1
            print('não tem estadão no link ---')
            continue

        # Pega o texto que acompanha o 'clicavel' - descrição
        descr = el.text.replace('\n', ' ')
        
        # Coleta o título e checa se o texto é o do botao - Se for, ele clica no botão
        title = el.get_attribute('title')

        # Coleta as outras informações do corpo da notícia
        imagem = (corpo.find_elements_by_tag_name('img'))
        isImagem = len(imagem)

        # Coleta a seção da notícia
        secaoNoticia = corpo.find_element_by_class_name('cor-e').text

        try:
            date = corpo.find_element_by_class_name('data-posts').text
        except:
            date = 'sem data'

        print(f'{i} - {title}')

        #Atribui o valor da imagem
        if isImagem == 0:
            isImagemtxt = 'Não tem imagem'
        elif isImagem == 1:
            imagem = imagem[0]
            isImagemtxt = imagem.get_attribute('src')
        else:
            isImagemtxt = 'Erro para verificar a imagem. l.166'

        # Cria o objeto da noticia no json
        data.append({
            'link': link,
            'title': title,
            'descr': descr,
            'date': date,
            'imagem': isImagemtxt,
            'secao': secaoNoticia
        }
        )

        #insere os valores no dicionário
        valores["ignoradas"] += contador

    # Pra cada notica, abre o artigo e puxa o conteudo
    for i in range(len(data)):
        print(f'{i+1} de {len(data)}')

        # Insere o link na posição i (notícia) do Json
        link = data[i]['link']
        try:
            br.get(link)
        except:
            print_exc()
            print(querylink)
            continue

        # Coleta de conteúdo. Verifica se o conteúdo está no Fullpath do HTML.
        content = ''
        time.sleep(.5)
        try:
            lista = []
            conteudo = 'erro no conteúdo'
            try:
                if(findElement('/html/body/section[2]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]/div[1]/div[3]')!= 0):
                    conteudo = GET('/html/body/section[2]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]/div[1]/div[3]')

                elif(findElement('/html/body/section[1]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]/div[1]/div[3]')!= 0):
                    conteudo = GET('/html/body/section[1]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]/div[1]/div[3]')

                elif(findElement('/html/body/section[2]/section/div[3]/div[2]/section/div/div/div/section/div/section[1]/div[1]/div[3]') != 0):
                    conteudo = GET('/html/body/section[2]/section/div[3]/div[2]/section/div/div/div/section/div/section[1]/div[1]/div[3]')

                elif(findElement('/html/body/section[3]/section/div[3]/div[2]/section/div/div/div/section/div/section[1]/div[1]/div[3]') != 0):
                    conteudo = GET('/html/body/section[3]/section/div[3]/div[2]/section/div/div/div/section/div/section[1]/div[1]/div[3]')
                
                elif(findElement('/html/body/section[3]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]/div[1]/div[3]') != 0):
                    conteudo = GET('/html/body/section[3]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]/div[1]/div[3]')
                
                elif(findElement('/html/body/div[4]/section/section/div[3]/section/div/div/div/section/div/section[1]/div[2]') != 0):
                    conteudo = GET('/html/body/div[4]/section/section/div[3]/section/div/div/div/section/div/section[1]/div[2]')

                elif(findElement('/html/body/section[1]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]/div[3]') != 0):
                    conteudo = GET('/html/body/section[1]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]/div[3]')

                # Estou coletando direto o H2 justamente porque não é <p>, então não coletará nada no for de baixo.
                elif(findElement('/html/body/section[2]/section/div[2]/div[1]/section/div/section/article/h2')!=0):
                    content = TXT('/html/body/section[2]/section/div[2]/div[1]/section/div/section/article/h2')

                # Se o conteúdo for diferente de erro, entra no for - pra cada <p> no conteudo, adiciona o texto do <p> na lista
                if conteudo != 'erro no conteúdo':
                    for paragrafo in conteudo.find_elements_by_tag_name('p'):
                        lista.append(paragrafo.text)
                    content = "\n".join(lista)  # Content recebe todo o conteúdo da lista "juntado"
            except:
                content = 'erro no conteúdo durante a coleta de dados'
                pass
        except:
            print_exc()
        data[i]['content'] = content
    print(querylink)

    return data, valor