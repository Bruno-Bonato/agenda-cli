import calendar
from datetime import date
import json
import os

#Funções de verificação


def mes_extenso(mes):
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro" ]
    return meses[mes-1]

def verificar_dia(dia,agenda):
    if not dia.isdigit() or int(dia) <= 0 or int(dia) > 31: #Confirindo se o algarismo digitado realmente é um número válido
        print("\n[SISTEMA] Por favor, digite uma data válida.\n")
        menu(agenda)

def verificar_mes(mes,agenda):
    if mes < 1 or mes > 12: #Confere se o alggorismo digitado realmente é um número válido
        print("\n[SISTEMA] Por favor, digite uma data válida.\n")
        menu(agenda)


#Funções de Menu e Organização

def menu(agenda):
    data = date.today() #Reconhece a data atual
    ano = data.year
    mes = data.month
    dia = data.day

    print(32*'-'+'AGENDA' + 32*'-')

    print(calendar.month(ano, mes)) #Imprime o Calendário do Mês 
    print("Hoje dia é", dia)
    print(32*'-')

    while True: #CRUD
        print("1 - Adiconar Evento")
        print("2 - Remover Evento")
        print("3 - Listar Eventos Futuros")
        print("4 - Sair")
        opcao = int(input("\nSelecione uma opção: "))
        
        if opcao == 4:
            salvar(agenda)
            break
        elif opcao == 1:
            adicionar_evento(agenda)
        elif opcao == 2:
            remover(agenda)
        elif opcao == 3:
            agenda = listar(agenda)

def ordenar(agenda):
    temp = {}
    for mes in agenda:
        ordena_mes = dict(sorted(agenda[mes].items())) #Usa a função 'items' para criar uma lista de pares chave-valor, a função 'sorted' ordena usando Timsort e a função 'dict' transforma em dicionário novamente
        temp[mes] = ordena_mes
    return temp


#Funções de Permanência de Dados

def salvar(agenda):
    with open("dados.json", "w", encoding="utf-8") as arquivo: #Cria e salva os dados no arquivo JSON
        json.dump(agenda, arquivo, indent = 4)
        print("Salavando e Fechando...")

def carregar_dados():
    if os.path.exists("dados.json"): #Carregando as informações do arquivo JSON caso exista
        with open("dados.json", "r") as arquivo:
            return json.load(arquivo)
    else:
        return { #Caso a 'agenda' não exista retornamos seu esqueleto 
            "janeiro": {},
            "fevereiro": {},
            "março": {},
            "abril": {},
            "maio": {},
            "junho": {},
            "julho": {},
            "agosto": {},
            "setembro": {},
            "outubro": {},
            "novembro": {},
            "dezembro": {}
        }  


#Funções do CRUD (Adicionar, Remover e Listar)

    
def adicionar_evento(agenda):
    dia = str(input("Quando será esse evento? *Em numeral* "))
    verificar_dia(dia,agenda)

    mes = int(input("Qual será o mês? *Em numeral* "))
    verificar_mes(mes,agenda)
    mes = mes_extenso(mes) #Transforma mês por extenso

    titulo = str(input("Digite o título do evento: ")).capitalize()
    comeco = str(input("Que horas começa? 00:00 "))
    final = str(input("Que horas termina? 00:00 "))
    descricao = str(input("Descição do Evento: ")).capitalize()

    agenda[mes][dia] = [titulo, comeco, final, descricao]
    print("\nEvento Adicionado\n")

def remover(agenda):
    if not agenda: #Verificando se à agenda não esta vazia
        print("\nA agenda esta vazia\n")
    
    dia = input("Qual o dia do vento que você deseja remover? *Em numeral* ")
    verificar_dia(dia,agenda)
    mes = int(input("Qual o mês do evento? *em numeral* "))
    verificar_mes(mes,agenda)
    mes = mes_extenso(mes) #Transforma mês por extenso

    if dia in agenda[mes]:
        agenda[mes].pop(dia)
        print("Evento deletado.")
    else:
        print("\n[SISTEMA] Não há evento nesta data\n")

def listar(agenda):
    agenda = ordenar(agenda)

    print("\n"+32*"-")
    print("1 - Listar próximos eventos\n2 - Eventos de um dia específico\n")
    escolha = int(input("Selecione uma opção:  "))

    if escolha == 1:
        for mes in agenda: 
            if agenda[mes] is not None: #Verificando se o mês não esta vazio
                for dia in agenda[mes]: 
                    if dia is not None: #Verifica se o dia não esta vazio
                        print(f"\n{agenda[mes][dia][0]}:\nDia {dia} de {mes} // {agenda[mes][dia][1]} - {agenda[mes][dia][2]}\nDescrição: {agenda[mes][dia][3]}\n")
    return agenda #Devolde a agenda ordena para a main
