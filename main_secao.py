import os  # importa o sistema
import json
import csv  # importa o CSV para gerar arquivos
import src.verify
import re
import traceback
import json
from src.interface import Iniciar
from datetime import datetime

# Faz a criação da pasta resultados
if not os.path.exists('./resultados'):
    os.makedirs('./resultados')

now = datetime.now()

nomearquivo, palavrachave, opcao, datainicial, datafinal, quantidade = Iniciar()

# Atribui as datas para as variáveis
DIAi = datainicial.split("/")[0]
MESi = datainicial.split("/")[1]
ANOi = datainicial.split("/")[2]

DIAf = datafinal.split("/")[0]
MESf = datafinal.split("/")[1]
ANOf = datafinal.split("/")[2]
qntdresult = 0

# Continua criando a pasta
dir_path = os.path.join(
    './resultados', f'{opcao} -  {palavrachave} - {ANOi} - {nomearquivo}')
if not os.path.exists(dir_path):
    os.makedirs(dir_path)


# Começa as pesquisas
results = []

if opcao == 'folha':
    import src.folhasp2 as site_atual
elif opcao == 'estadao':
    import src.estadao3 as site_atual
elif opcao == 'uol':
    import src.uol as site_atual
else:
    raise ValueError('Site Invalido')

inicioh = now.hour
iniciom = now.minute

print(f"Hora inicial: {inicioh}:{iniciom}")
# Realiza a pesquisa
try:
    pesquisa, valor = site_atual.search(
        query=palavrachave, DIAi=DIAi, MESi=MESi, ANOi=ANOi, DIAf=DIAf, MESf=MESf, ANOf=ANOf)
    print(
        f'Finalização da pesquisa -- Nome do arquivo: {opcao} - {palavrachave} - {ANOi} - {nomearquivo}')
finally:
    site_atual.END()
# Pra cada resultado da pesquisa, adiciona o resultado na lista 'results'
for search_result in pesquisa:
    results.append(search_result)

def setfy(data, key):
    visited = set([])
    setfied = []

    for element in data:
        if element[key] not in visited:
            visited.add(element[key])
            setfied.append(element)

    return setfied

results = setfy(results, 'title')

# Faz o preenchimento de arquivos (todos)
# Preenche um CSV com os resultados obtidos (Título, Data, descrição e link)
with open('{}.csv'.format(os.path.join(dir_path, "Resultados_da_coleta")), 'w',  encoding='utf-8') as csv_file:
    for res in results:
        if(opcao == 'estadao'):
            res['date'] = res['date'].replace('|', '-')
            res['secao'] = res['secao'].replace('?', '')
            res['secao'] = res['secao'].replace('!', '')
            res['secao'] = res['secao'].replace(':', '')
            res['secao'] = res['secao'].replace('/', '')
            res['secao'] = res['secao'].replace('\'', '')
            res['secao'] = res['secao'].replace('|', '')

        # res['secao'] = unicodedata.normalize("NFD", res['secao'])
        # res['secao'] = res['secao'].encode("ascii", "ignore")
        # res['secao'] = res['secao'].decode("utf-8")
        csv_file.write((res['date'] + '\t' + res['title'] + '\t' + res['secao'] + '\t' +
                        res['imagem'] + '\t' + res['descr'] + '\t' + res['link']).replace('\n', ' '))
        csv_file.write('\n')
        arquivotxt = re.sub('\W', '_', res['title'])
        sec_path = os.path.join(dir_path, res['secao'])
        if not os.path.exists(sec_path):
            os.makedirs(sec_path)
        with open('{}.txt'.format(os.path.join(sec_path, res['date'] + ' - ' + arquivotxt[:20])), 'w', encoding='utf-8') as text:
            res['content'] = re.sub('\n+', '\n', str(res['content']))
            try:
                content = res['title'] + '\n\n' + res['content']
            except KeyError:
                content = 'Algo deu errado - main l.101 KeyError - Informar ao desenvolvedor'
            text.write(content)
            qntdresult += 1
            # Gera o arquivo de coleta
with open('{}.txt'.format(os.path.join(dir_path, "Parâmetros_da_coleta")), 'w', encoding='utf-8') as text:
    text.write(f'Nome da pasta: {opcao} -  {palavrachave} - {ANOi} - {nomearquivo}\nPalavra chave: {palavrachave}\nSite: {opcao}\nData inicial: {datainicial}\nData final: {datafinal}\nNotícias encontradas (no site): {valor}\nResultados obtidos: {qntdresult}')

end = datetime.now()
fimh = end.hour
fimm = end.minute

diferencah = fimh - inicioh
diferencam = fimm - iniciom
print("\n\n-----------------------------------------------------")
print(f"Horário inicial da pesquisa: {inicioh}:{iniciom}")
print(f"Horário final da pesquisa: {fimh}:{fimm}")
print(f"Tempo percorrido: {diferencah}:{diferencam}\n--------------------------------------------------------------\n\n")