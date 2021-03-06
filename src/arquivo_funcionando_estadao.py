from src.browser import *
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import traceback

# with open(os.path.join('src', 'main.js')) as infile:
# 	elimn_assin = infile.read()


def search(query, DIAi, MESi, ANOi, DIAf, MESf, ANOf):
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
    br.get(
        f'https://busca.estadao.com.br/?tipo_conteudo=&quando={DIAi}%2F{MESi}%2F{ANOi}-{DIAf}%2F{MESf}%2F{ANOf}&q={query}')

    # Pega a quantidade de resultados da pesquisa
    try:
        secaoqntd = TXT('/html/body/section[3]/div/section/form/section/div/p')
        valor = int(secaoqntd.split(' ')[2])
    except:
        valor = 30

    calculopage = int(valor/10)

    # Clica em ACEITAR as politicas de cookies
    time.sleep(4)
    try:
        CLICK('/html/body/div[6]/div/div/div[2]/button') 
    except:
        try:
            CLICK('/html/body/div[6]/div/div[2]/button')
        except:
            pass

    # Tenta ja expandir a primeira vez os resultados - O primeiro botao de "carregar mais" se comporta diferente dos demais
    br.execute_script("window.scrollTo(0, 1080)")
    time.sleep(3)

    # Clica no primeiro botão que é difernete dos demais
    try:
        CLICK('/html/body/section[4]/div/section[1]/div/section[2]/div/a')
    except:
        try:
            print('entro uno segundo try')
            GET('/html/body/section[4]/div/section[1]/div/section[2]/div/a').click()
        except:
                try:
                    CLASS('go more-list-news btn-mais fn brd-e').click()
                except:
                    print('erro no click do botão---------------------------------')

    data = []
    i = 0
    c = 0
    contador = 0
    isImagem = False
    noticias = 10
    print(f'Valor: {valor}')
    onedivmore = ' '
    corpo = ' '
    divisorias = 'section[1]/div/div'
    botaodiv = '/section[1]/div/div'
    apertei = 0

    pagina = 1

    # =====================================================================================================================
    while c < valor:
        corpo = ' '
        i += 1
        c += 1

        # Tenta pegar um 'clicavel' novo
        try:
            if(corpo == ' ' and i==11):
                i = 1
                divs = '/html/body/section[4]/div/section[1]/div/div/div/'
                onedivmore = divisorias.join(divs.split('section[1]/div'))
                divisorias = divisorias + '/div'
            
            corpo2 = onedivmore + f'section[{i}]'
            if(onedivmore != ' ' and findElement(corpo2) != 0):
                corpo = corpo2
                corpo = WAIT_GET(corpo)

            if(corpo == ' ' and findElement(f'/html/body/section[4]/div/section[1]/div/div/section[{i}]') != 0):
                corpo = WAIT_GET(f'/html/body/section[4]/div/section[1]/div/div/section[{i}]')
        except:
            # Se nao tiver, acabou todas as noticias ou deu erro :/
            print('break linha 103')
            break

        # Tenta clicar no botão de Carregar Mais - a cada 10 notícias        
        if(i==10 and apertei<=calculopage):
            try:
                GET(f'/html/body/section[4]/div/section[1]/div/div/section[11]/div/a').click()
            except:
                try:
                    botoes = f'/html/body/section[4]/div/section[1]/div/div/section[11]/div/a'
                    onemorebutton = botaodiv.join(botoes.split('/section[1]/div'))
                    botaodiv = botaodiv + '/div'
                    GET(onemorebutton).click()
                    pagina += 1
                except:
                    print_exc()
                    break
            apertei+=1
        time.sleep(1)
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
            print(f' Filtrou conteudo: {contador}')
            continue

        if 'estadao' not in link:
            c -= 1
            print('não tem estadão no link ---')
            continue

        # Pega o texto que acompanha o 'clicavel' - descrição
        descr = el.text.replace('\n', ' ')
        # Coleta o título e checa se o texto é o do botao - Se for, ele clica no botão
        title = el.get_attribute('title')
        # if title == 'Carregar mais':
        #     el.click()
        #     continue

        # Coleta as outras informações do corpo da notícia
        isImagem = len(corpo.find_elements_by_tag_name('img'))
        secaoNoticia = corpo.find_element_by_class_name('cor-e').text
        date = corpo.find_element_by_class_name('data-posts').text

        print(f'{i} - {title}')

        #Atribui o valor da imagem
        if isImagem == 0:
            isImagemtxt = 'Não tem imagem'
        elif isImagem == 1:
            isImagemtxt = 'Tem imagem'
        else:
            isImagemtxt = 'Erro para verificar a imagem. l.174'

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
    # Pra cada notica, abre o artigo e puxa o conteudo
    for i in range(len(data)):
        print(i)

        # Insere o link na posição i (notícia) do Json
        link = data[i]['link']
        try:
            br.get(link)
        except:
            print_exc()
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

    return data, valor