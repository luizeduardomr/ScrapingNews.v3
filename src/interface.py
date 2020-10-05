import os
import PySimpleGUI as sg

sg.change_look_and_feel('DarkAmber')  # colour

# layout of window
layout = [
    [sg.Frame(layout=[
        [sg.Radio('1. Estadão', 1, default=False, key='estadao'),
         sg.Radio('2. Folha', 1,
                     default=False, key='folha'),
         sg.Radio('3. Uol Notícias', 1, default=False, key='uol')]],
        title='Selecione o site para a pesquisa', title_color='white',
        relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Caso o site selecionado seja o Estadão ou Folha, indique as datas de início e término da pesquisa.\nCaso o site seja o Uol, indique o valor da quantidade de resultados para coletar')],
    [sg.Text('Nome do arquivo:'), sg.InputText(key='nomearquivo')],
    [sg.Text('Palavras chaves:'), sg.InputText(key='palavrachave')],
    [sg.Text('Data inicial: (ex: 01/01/2010)'), sg.InputText(key='datainicial')],
    [sg.Text('Data final: (ex: 06/04/2020'), sg.InputText(key='datafinal')],
    [sg.Text('Quantidade de resultados (ex: 4)'), sg.InputText(key='quantidade')],


    [sg.Submit('Pesquisar'), sg.Button('Cancelar')],
]

window = sg.Window('Mudanças Climáticas Search', layout)  # make the window

event, values = window.read()


def Iniciar():
    nomearquivo = values['nomearquivo']
    palavrachave = values['palavrachave']
    datainicial = values['datainicial']
    datafinal = values['datafinal']
    quantidade = values['quantidade']
    count = 0
    if(nomearquivo ==''):
        nomearquivo = len(os.listdir('resultados')) +1
        nomearquivo = f'coleta{nomearquivo}'
    if(datainicial == '' and datafinal == ''):
        datainicial = '01/01/2011'
        datafinal = '01/01/2012'
    if(palavrachave == ''):
        palavrachave = 'Mudanças climáticas'
    if(quantidade == ''):
        quantidade = 5
    while count == 0:
        if event in (None, 'Cancelar'):
            count+=1
            return 'Cancelou o programa'
        elif values['estadao'] == True:
            opcao = 'estadao'
            count+=1
        elif values['folha'] == True:
            opcao = 'folha'
            count+=1
        elif values['uol'] == True:
            opcao = 'uol'
            count+=1
    return nomearquivo, palavrachave, opcao, datainicial, datafinal, quantidade