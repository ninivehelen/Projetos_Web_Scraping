import requests
# Biblioteca para fazer a requisição da pagina
from bs4 import BeautifulSoup
# Biblioteca para manipular e selecionar dados do html
import json
# Biblioteca para salvar o arquivo em json

pagina = requests.get(
    "https://www.gov.br/ana/pt-br/acesso-a-informacao/agenda-de-autoridades")
# Requisição na pagina Inicial

content = pagina.content

site = BeautifulSoup(content, "html.parser")
# BeautifulSoup para acessar o site e manipular e selecionar dados do html.

dados_agenda = []  # Lista para alocar os dados extraidos e estruturar.
for link in site.findAll('a', attrs={'class': 'internal-link'}):
    # Codigo para acessar os links da pagina principal para acessar.
    pagina1 = requests.get(link.get('href'))
# Requisicao dos links
    content1 = pagina1.content
    site1 = BeautifulSoup(content1, "html.parser")
# Acessando a pagina para conseguir acessar os links da pagina utilizando BeautifulSoup
    for link2 in site1.findAll('a', attrs={'class': 'internal-link'}):
        # Codigo para acessar os links extraidos da pagina anterior para acessar.
        pagina2 = requests.get(link2.get('href'))
# Requisicao dos links
        content2 = pagina2.content
        site2 = BeautifulSoup(content2, "html.parser")
# Acessando a pagina para manipular e extrair dados do html com o BeautifulSoup
# Iniciando a extração dos dados agora que está na pagina que contem as informaçoes a ser extraida
        data = site2.find(class_="day is-selected has-appointment")
        if data is not None:
            data = data.get('data-day')
# Extraindo a data, e usando comando if para tratar dados que contém none, evitando erros e exceçoes.
        for agenda in site2.findAll('div', attrs={'id': 'wrapper'}):
            nome = agenda.find(
                'div', attrs={'class': "documentDescription description"})
            nome1 = agenda.find(
                'div', attrs={'class': "pessoa-nome"})
            nome2 = agenda.find(
                'h1', attrs={'class': "documentFirstHeading"})
# Extraindo o nome da autoridade, foi necessario usar varias variaveis já que o html nao estava no padrao para todos os nomes.
            if nome is not None:
                nome = nome.text
            elif nome1 is not None:
                nome = nome1.text
            elif nome1 is not None:
                nome = nome2.text
# Condição para tratar os nomes, ja que nao estava no padrao todos os html que continha os nomes das autoridades.
            cargo = agenda.find(
                'div', attrs={'class': "pessoa-cargo"})
            cargo1 = agenda.find(
                'h1', attrs={'class': "documentFirstHeading"})
# Extraindo o cargo da autoridade, foi necessario usar varias variaveis já que o html nao estava no padrao para todos os cargos.
            if cargo is not None:
                cargo = cargo.text
            elif cargo1 is not None:
                cargo = cargo1.text
# Condição para tratar os cargos, ja que não estava no padrao todos os html que continha os cargos das autoridades.
            for agenda in site2.findAll('li', attrs={'class': "item-compromisso-wrapper"}):
                nome_compromisso = agenda.find(
                    'h4', attrs={'class': "compromisso-titulo"})
                horario_inicio = agenda.find(
                    'time', attrs={'class': "compromisso-inicio"})
                horario_inicio = horario_inicio.text
                horario_fim = agenda.find(
                    'time', attrs={'class': "compromisso-fim"})
# Codigo para extrair horarios da agenda das autoridades, de inicio e fim.
                if horario_fim is not None:
                    horario_fim = horario_fim.text
                else:
                    horario_fim = " "
# Codigo para tratar exceçoes e evitar erro, ja que nao era todas as agendas continha a data final do evento.
                local_evento = agenda.find(
                    'div', attrs={'class': "compromisso-local"})
# Codigo para extrair locais da agenda das autoridades.
                if local_evento is not None:
                    local = local_evento.text
                else:
                    local = " "
# Codigo para tratar exceçoes e evitar erro, caso tivesse alguma agenda sem nome do local.
                dados_agenda.append({
                    "Nome da Autoridade": nome,
                    "Cargo da Autoridade": cargo,
                    "Data E Horário:": data+' '+horario_inicio+'-'+horario_fim,
                    "Nome do Evento:": nome_compromisso.text,
                    "Local Evento:": local,
                })
# Codigo para Salvar os dados, utilizando a lista que foi criada no inicio do codigo, assim podendo.....
# estruturar melhor os dados na hora de salvar no json.
                print(dados_agenda)
# Codigo para printar a lista no console, assim podendo ver quando o algoritmo encerar e mostrando se esta
# funcionando antes de checar o json.
        with open('Agenda_Autoridades.json', 'w', encoding='utf-8') as fp:
            json.dump(dados_agenda, fp, indent=3, ensure_ascii=False)
# Codigo para salvar os dados em json, que foram extraídos e adionados a lista. Agora estão
# também em um arquivo json.  UTF-8 para os dados serem salvos reconhecendo as acentuaçoes.
