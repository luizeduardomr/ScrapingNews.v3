from src.browser import *
import time
import re
import os

with open(os.path.join('src', 'main.js')) as infile:
    elimn_assin = infile.read()


def clear(x): return re.sub('\s+', ' ', x.text.replace('\n', ' '))


def search(query):

    br = GLOBAL_BR
    query = query.replace(' ', '+')
    # Realiza a busca

    # https://search.folha.uol.com.br/search?q=Mudanças+climáticas&periodo=personalizado&sd=05%2F04%2F2020&sd=&ed=03%2F08%2F2020&ed=&site=todos
    # br.get('https://search.folha.uol.com.br/?q={}&site=todos'.format(query.replace(' ', '+')))
    # br.get(f'https://search.folha.uol.com.br/search?q={query}&periodo=personalizado&sd={DIAi}%2F{MESi}%2F{ANOi}&sd=&ed={DIAf}%2F{MESf}%2F{ANOf}&ed=&site=jornal')

    # filtro por ano (personalizado é bugado de mais)
    #br.get(f'https://search.folha.uol.com.br/search?q={query}&periodo=ano&sd=&sd=&ed=&ed=&site=todos')
    
    br.get(f'https://search.folha.uol.com.br/search?q={query}&periodo=personalizado&sd={DIAi}%2F{MESi}%2F{ANOi}&ed={DIAf}%2F{MESf}%2F{ANOf}&site=todos')

    br.execute_script(elimn_assin)

    try:
        secaoqntd = TXT(
            '/html/body/main/div/div/form/div[2]/div/div/div[2]/div[2]/div[1]'  )
        valor = int(secaoqntd.split(' ')[0])
        print(valor)
    except:
        valor = 5

    data = []

    i = 0
    c = 0
    count = 1
    while c < valor:
        i += 1
        c += 1
        count += 1

        # Tenta pegar a proxima noticia
        try:
            if(findElement(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]/div[3]/div/a') != 0):
                el = WAIT_GET(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]/div[3]/div/a')

            elif(findElement(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]/div[2]/div/a') != 0):
                el = WAIT_GET(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]/div[2]/div/a')
        except:
            # Se nao tiver, tenta avancar para a proxima pagina
            try:
                pags = GET(
                    '//*[@id="conteudo"]/div/div/form/div[2]/div/div/div[2]/nav/ul').find_elements_by_tag_name('li')

                # Ve se ainda tem uma 'pagina seguinte'
                if pags[-1].text.strip() == '':
                    pags[-1].click()
                    i = 0
                    continue
                else:  # Senao chegou ao fim
                    pass

            except:  # Nao tem pagina seguinte, eh so uma pagina de resultados
                pass

        # Pega as informacoes do headline da noticia
        descr = clear(el)
        descr = descr[:descr.rindex('...')+3]

        link = el.get_attribute('href')
        title = clear(el.find_element_by_class_name('c-headline__title'))
        date = el.find_element_by_tag_name('time').get_attribute('datetime')

        if findElement(f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{count}]/div[2]/div/a/img') != 0:
            isImagemtxt = 'Tem imagem'
        else:
            isImagemtxt = 'Não tem imagem'
        count +=1   
        #/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[1]/div[2]/div/a/img
        #/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[2]/div[2]/div/a/img
        data.append({
            'link': link,
            'title': title,
            'descr': descr,
            'date': date,
            'imagem': isImagemtxt
        }
        )

    # Para cada notica, abre o artigo e puxa o conteudo
    for i in range(len(data)):
        link = data[i]['link']
        br.get(link)
        content = ''
        try:
            lista = []
            conteudo = 'erro no conteúdo'
            try:
                    
                if(findElement('/html/body/div[3]/main/article/div[5]/div/div/div/div/div[2]/div/div[1]')!= 0):
                    conteudo = GET('/html/body/div[3]/main/article/div[5]/div/div/div/div/div[2]/div/div[1]')
                
                elif(findElement('/html/body/div[3]/main/article/div[5]/div/div/div/div/div[2]/div[4]/div[1]')!= 0):
                    conteudo = GET('/html/body/div[3]/main/article/div[5]/div/div/div/div/div[2]/div[4]/div[1]')

                elif(findElement('/html/body/div[5]/div/div[1]/article/div[3]') != 0):
                    conteudo = GET('/html/body/div[5]/div/div[1]/article/div[3]')
                
                elif(findElement('/html/body/div[3]/main/article/div[5]/div/div/div/div/div[2]/div/div[2]') != 0):
                    conteudo = GET('/html/body/div[3]/main/article/div[5]/div/div/div/div/div[2]/div/div[2]')

                elif(findElement('/html/body/div[3]/main/article/div[5]/div/div/div/div/div[2]/div[1]/div[2]') != 0):
                    conteudo = GET('/html/body/div[3]/main/article/div[5]/div/div/div/div/div[2]/div[1]/div[2]')
                elif(findElement('/html/body/div[3]/main/article/div[5]/div/div/div/div/div[2]/div[2]/div[2]') != 0 ):
                    conteudo = GET('/html/body/div[3]/main/article/div[5]/div/div/div/div/div[2]/div[2]/div[2]')

                elif(findElement('/html/body/div[2]/div[2]/div/main/div/div/div/div/article/div/div[2]') != 0):
                    conteudo = GET('/html/body/div[2]/div[2]/div/main/div/div/div/div/article/div/divconteudo[2]')

                elif(findElement('/html/body/div[7]/div/div[1]/article/div[3]') != 0):
                    conteudo = '\n'.join(GET('/html/body/div[7]/div/div[1]/article/div[3]').find_elements_by_tag_name('p'))

                    
                if conteudo != 'erro no conteúdo':
                    for paragrafo in conteudo.find_elements_by_tag_name('p'):
                        lista.append(paragrafo.text)
                    content = "\n".join(lista)
            except:
                conteudo = 'erro no conteúdo durante a coleta de dados'
                pass
        except:
            print_exc()
        data[i]['content'] = content

    return data, valor

    #     try:
    #         content = WAIT_CLASS('c-news__body').text
    #     except:
    #         try:
    #             content = TXT('//*[@id="conteudo"]/div[3]')
    #         except:
    #             pass

    # return data, valor
