from os import link
from src.browser import *
import time
import re
import os
import traceback
from selenium.webdriver.common.action_chains import ActionChains

with open(os.path.join('src', 'main.js')) as infile:
	elimn_assin = infile.read()

def clear(x): return re.sub('\s+', ' ', x.text.replace('\n', ' '))

# def clear2(x):
#     return x.find_element_by_tag_name('p')

def search(query, DIAi, MESi, ANOi, DIAf, MESf, ANOf):

    br = GLOBAL_BR  
    query = query.replace(' ', '+')

    # Entra com a conta
    br.get('https://login.folha.com.br/login?service=paywall%2Ffrontend&done=https%3A%2F%2Fwww.folha.uol.com.br%2F')
    time.sleep(2)
    try:
        GET('/html/body/main/section/div[2]/div/div[1]/div/div/form/div[1]/input').send_keys('luizdudumr@gmail.com')
        GET('/html/body/main/section/div[2]/div/div[1]/div/div/form/div[2]/input').send_keys('SenhaPraias0')
        time.sleep(.5)
        try:
            GET('/html/body/main/section/div[2]/div/div[1]/div/div/form/div[4]/button').click()
        except:
            print_exc()
    except:
        pass
    time.sleep(2)

    querylink = f'https://search.folha.uol.com.br/search?q={query}&periodo=personalizado&sd={DIAi}%2F{MESi}%2F{ANOi}&ed={DIAf}%2F{MESf}%2F{ANOf}&site=todos'
    br.get(querylink)
    time.sleep(3)
    br.execute_script(elimn_assin)

    print(querylink)
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

    # Clica para aceitar os Cookies (TEMPORÁRIO)
    if(clickNow('/html/body/div[11]/div/div[2]/button') == 0):
        try:
            CLICK('/html/body/div[11]/div/div[2]/button')
        except:
            try:
                CLASS('banner-lgpd-consent__accept').click()
            except:
                print('erro pra clicar nos Cookies')
                pass

        br.execute_script('window.scrollTo(0,document.body.scrollHeight)')

    while c < valor:
        br.execute_script("window.scrollTo(0, 2560)")
        i += 1 #label da notícia
        c += 1
        # Verifica se está no fim da página
        if(i==26):
            print('\n')
            # Verifica se ainda tem o botão para ir para a próxima página
            # Se tiver, ele clica. Senão, significa que acabaram as notícias
            if(findClass('c-pagination__arrow') != 0):
                try:
                    br.find_elements_by_class_name('c-pagination__arrow')[-1].click()
                except:
                    try:
                        br.find_elements_by_class_name('c-pagination__arrow')[1].click()
                    except:
                        print('erro pra mudar de página......................................')
                        pass
                i = 0
                continue
                time.sleep(1)
            else:
                print('erro pra pular de página-------------------------------------')
        # Tenta pegar a proxima noticia
        try:
            if(findElement(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]') != 0):
                corpoglobal = WAIT_GET(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]')
            elif(findElement(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]') != 0):
                corpoglobal = WAIT_GET(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]')                
        except:
            # Se nao tiver, tenta avancar para a proxima pagina
            if(findElement('/html/body/main/div/div/form/div[2]/div/div/div[2]/nav/ul/li[8]/a') != 0):
                CLICK('/html/body/main/div/div/form/div[2]/div/div/div[2]/nav/ul/li[8]/a')
            else:
                pass

        # Pega as informacoes do headline da noticia
        try:
            descr = corpoglobal.find_element_by_tag_name('p').text
        except:
            try:
                descr = corpoglobal.find_element_by_tag_name('b').text
            except:
                descr = 'Não há descrição nesta notícia'
        
        link = ''
        title = ''
        date = ''
        secaoNoticia= ''
        try:
            link = corpoglobal.find_element_by_tag_name('a').get_attribute('href')
            title = clear(corpoglobal.find_element_by_class_name('c-headline__title'))
            date = corpoglobal.find_element_by_tag_name('time').get_attribute('datetime')
            secaoNoticia = corpoglobal.find_element_by_tag_name('h3').text
        except:
            print('erro pra coletar link, título, data ou seção da notícia')
            print(f'Notícia atual: {i} --- {link}')
            pass

        
        # descr = clear(el.find_element_by_tag_name('p'))
        # print([x.text for x in corpoglobal.find_elements_by_tag_name('p')])

        # Altera a ordem da data (12.nov.2019 às 13h01) 
            # [12] [nov] [2019 às 13h01]
        #date = date.split('.')

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
            'secao': secaoNoticia,
        }
        )

        time.sleep(.5)
    # Para cada notica, abre o artigo e puxa o conteudo
    for i in range(len(data)):
        print(f'{i+1} de {len(data)}')
        link = data[i]['link']
        br.get(link)
        lista = []
        content = 'não pegou o conteúdo'
        try:
            conteudo = 'erro no conteúdo'
            conteudo = wait(
                lambda: CLASS('c-news__body'),
                lambda: CLASS('js-news-content'),
                lambda: CLASS('c-news__content')
                #lambda: CLASS('content')
                )
            # Se o conteúdo for diferente de erro, entra no for - pra cada <p> no conteudo, adiciona o texto do <p> na lista
            if conteudo != 'erro no conteúdo':
                # print('conteudo entrou no if != erro no conteúdo --- logo vai coletar o p')
                for paragrafo in conteudo.find_elements_by_tag_name('p'):
                    lista.append(paragrafo.text)
                content = "\n".join(lista)  # Content recebe todo o conteúdo da lista "juntado"
        except:
            try:
                    if(findElement('/html/body/table[5]/tbody/tr/td[2]/') != 0):
                        conteudo = GET('/html/body/table[5]/tbody/tr/td[2]/')

                    elif(findElement(f'/html/body/table[5]/tbody/tr/td[2]')!=0):
                        conteudo = GET(f'/html/body/table[5]/tbody/tr/td[2]')

                    elif(findElement(f'/html/body/div[1]/div[1]/div[8]/div')!=0):
                        conteudo = GET(f'/html/body/div[1]/div[1]/div[8]/div')

                    elif(findElement(f'/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/article/div[2]')!=0):
                        conteudo = GET(f'/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/article/div[2]')

                    elif(findElement('/html/body/main/article/div[1]/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div[3]')!=0):
                        conteudo = GET('/html/body/main/article/div[1]/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div[3]')

                    elif(findElement(f'/html/body/div[1]/div[6]/div')!=0):
                        conteudo = GET(f'/html/body/div[1]/div[6]/div')

                    elif(findElement(f'/html/body/div[1]/div/div[8]/div')!=0):
                        conteudo = GET(f'/html/body/div[1]/div/div[8]/div')

                    elif(findElement('/html/body/div[2]/div[2]/div[1]/div[2]/div') != 0):
                        conteudo = GET('/html/body/div[2]/div[2]/div[1]/div[2]/div')
                    
                    elif(findElement('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/article/div[2]') != 0):
                        conteudo = GET('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/article/div[2]')
                    # Se o conteúdo for diferente de erro, entra no for - pra cada <p> no conteudo, adiciona o texto do <p> na lista
                    if conteudo != 'erro no conteúdo':
                        # print('conteudo entrou no if != erro no conteúdo --- logo vai coletar o p')
                        for paragrafo in conteudo.find_elements_by_tag_name('p'):
                            lista.append(paragrafo.text)
                        content = "\n".join(lista)  # Content recebe todo o conteúdo da lista "juntado"
            except:
                content = 'Erro durante a coleta de conteúdo'
                print('\n\nErro na coleta ----------------------------------')
                print(f'{link}\n\n')
        data[i]['content'] = content

    return data, valor

            # if(i == 26):
            # print('\n')
            # # Verifica se ainda tem o botão para ir para a próxima página
            # # Se tiver, ele clica. Senão, significa que acabaram as notícias
            # if(findClass('c-pagination__arrow') != 0):
            #     try:
            #         br.find_elements_by_class_name('c-pagination__arrow')[-1].click()
            #     except:
            #         try:
            #             br.find_elements_by_class_name('c-pagination__arrow')[1].click()
            #         except:
            #             print('erro pra mudr de página...')
            #             pass

            #     i = 0
            #     print(f'================= entrou no if l.64 --- Valor do i:  {i} ========================')
            #     continue
            #     time.sleep(.10)
            # else:
            #     print('erro pra pular de página-------------------------------------')









            #             for x in range(8, 2, -1):
            #     try:
            #         if(findElement(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/nav/ul/li[{x}]/a')) != 0:
            #             try:
            #                 CLICK(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/nav/ul/li[{x}]/a')
            #             except:
            #                 print_exc()
            #         else:
            #             continue
            #     except:
            #         print(f'{x} - erro pra mudar de páginaaaaaaaaa')
            # i = 0
            # continue