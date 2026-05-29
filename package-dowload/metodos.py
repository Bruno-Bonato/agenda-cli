from datetime import datetime
from rich import print
from rich.console import Console
import calendar
from datetime import date
import json
import os

console = Console()
# Funções de verificação


def verificar_hora(hora):  # Verifica se a hora informada é válida
    try:
        datetime.strptime(hora, "%H:%M").time()
    except ValueError:
        print("\n[red][SISTEMA] Digite uma hora válida.\n")
    else:
        return True


# Verifica se já existe um evento com mesmo títuo neste dia
def verifica_titulo(agenda, mes, dia, titulo):
    for evento in agenda[mes][dia]:
        if evento[0] == titulo:
            return True
    return False

def mes_extenso(mes):
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
             "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    return meses[mes-1]

def verifica_existencia_dia(agenda,dia,mes): #Verifica se já existe lista para um dia específico
    if dia not in agenda[mes]:
        return True
    else:
        return False
        

def verificar_dia(dia, agenda):
    # Confirindo se o algarismo digitado realmente é um número válido
    if not dia.isdigit() or int(dia) <= 0 or int(dia) > 31:
        print("\n[red][SISTEMA] Por favor, digite uma data válida.\n")
        return False


def verificar_mes(mes, agenda):
    if mes < 1 or mes > 12:  # Confere se o alggorismo digitado realmente é um número válido
        print("\n[red][SISTEMA] Por favor, digite uma data válida.\n")
        return False


def verificar_agenda(agenda):  # Veifica se a agenda esta vazia
    if sum(len(agenda[mes]) for mes in agenda) == 0:
        print("\n[red][SISTEMA] A agenda está vazia.\n")
        return False
    else:
        return True

# Funções de Menu e Organização

def menu(agenda):
    data = date.today()  # Reconhece a data atual
    ano = data.year
    mes = data.month
    dia = data.day

    print(32*'-'+'AGENDA' + 32*'-')

    print(calendar.month(ano, mes))  # Imprime o Calendário do Mês
    print("Hoje dia é", dia)
    print(32*'-')

    while True:  # CRUD
        print("[blue cyan]1 - Adiconar Evento")
        print("[blue cyan]2 - Remover Evento")
        print("[blue cyan]3 - Listar Eventos Futuros")
        print("[blue cyan]4 - Sair")
        try:
            opcao = int(console.input(
                "\n[blink]Selecione uma opção: *em numeral* "))
        except ValueError:
            print("\n[red][SISTEMA] Digite um número válido.\n")
            menu(agenda)

        if opcao == 4:
            salvar(agenda)
            break
        elif opcao == 1:
            adicionar_evento(agenda)
        elif opcao == 2:
            remover(agenda)
        elif opcao == 3:
            agenda = listar(agenda)
        else:
            print("\n[red][SISTEMA] Digite uma opção válida.\n")


def ordenar(agenda):
    temp = {}
    for mes in agenda:
        # Usa a função 'items' para criar uma lista de pares chave-valor, a função 'sorted' ordena usando Timsort e a função 'dict' transforma em dicionário novamente
        ordena_mes = dict(sorted(agenda[mes].items()))
        temp[mes] = ordena_mes
    return temp


# Funções de Permanência de Dados

def salvar(agenda):
    # Cria e salva os dados no arquivo JSON
    with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(agenda, arquivo, indent=4)
        print("\n[green]Salavando e Fechando...\n")


def carregar_dados():
    # Carregando as informações do arquivo JSON caso exista
    if os.path.exists("dados.json"):
        with open("dados.json", "r") as arquivo:
            return json.load(arquivo)
    else:
        return {  # Caso a 'agenda' não exista retornamos seu esqueleto
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


# Funções do CRUD (Adicionar, Remover e Listar)


def adicionar_evento(agenda):
    dia = str(console.input(
        "\n[blue cyan]Qual é o dia desse evento? *Em numeral* "))
    verificar_dia(dia, agenda)

    mes = int(console.input("[blue cyan]Qual será o mês? *Em numeral* "))
    verificar_mes(mes, agenda)
    mes = mes_extenso(mes)  # Transforma mês por extenso

    titulo = str(console.input(
        "[blue cyan]Digite o título do evento: *ENTER para pular* ")).capitalize()
    comeco = str(console.input("[blue cyan]Que horas começa? 00:00 "))
    verificar_hora(comeco)

    final = str(console.input("[blue cyan]Que horas termina? 00:00 "))
    verificar_hora(final)

    descricao = str(console.input(
        "[blue cyan]Descição do Evento: *ENTER para pular* ")).capitalize()

    if verifica_existencia_dia(agenda,dia,mes): #Checa se ja há eventos no dia, se não, ele cria a lista para armazenar
        agenda[mes][dia] = []
        agenda[mes][dia].append([titulo, comeco, final, descricao])
    else:
        agenda[mes][dia].append([titulo, comeco, final, descricao])

    print("\n[green][SISTEMA] Evento Adicionado\n")


def remover(agenda):
    verificar_agenda(agenda)

    dia = console.input(
        "[blue cyan]Qual o dia do vento que você deseja remover? *Em numeral* ")
    verificar_dia(dia, agenda)
    mes = int(console.input("[blue cyan]Qual o mês do evento? *em numeral* "))
    verificar_mes(mes, agenda)
    mes = mes_extenso(mes)  # Transforma mês por extenso

    if dia in agenda[mes]:
        if len(agenda[mes][dia]) == 1:  # Verifica se Há apenas um evento
            agenda[mes].remove(dia)
            print("\n[green][SISTEMA] Evento deletado.\n")
        else:
            # Pegunta o título do evento para o usuário
            titulo = str(console.input(
                "[blue cyan]Qual o título do evento que deseja remove? ")).capitalize()
            if not verifica_titulo(agenda, mes, dia, titulo):
                print("\n[red][SISTEMA] Não há evento com este título\n")
                menu(agenda)
            else:
                # Procura pelo evento e o remove, sem altera o resto dos eventos do dia.
                for evento in agenda[mes][dia]:
                    if evento[0] == titulo:
                        print("\n[green][SISTEMA] Evento deletado.\n")
                        agenda[mes][dia].remove(evento)
                        break
    else:
        print("\n[red][SISTEMA] Não há evento nesta data ou com este título\n")


def listar(agenda):
    agenda = ordenar(agenda)

    print("\n"+32*"-")
    print("[blue cyan]1 - Listar próximos eventos\n[blue cyan]2 - Eventos de um dia específico\n")
    escolha = int(console.input("[blink]Selecione uma opção:  "))

    if escolha == 1:
        if verificar_agenda(agenda):  # Verifica se a agenda ta fazia  Obs: A agenda vazia tem 12 itens
            for mes in agenda:
                if agenda[mes]:  # Verificando se o mês não esta vazio
                    for dia in agenda[mes]:
                        if agenda[mes][dia]:  # Verifica se o dia não esta vazio
                            for evento in agenda[mes][dia]:
                                print(f"\n{evento[0]}:\nDia {dia} de {mes} // {evento[1]} - {evento[2]}\nDescrição: {evento[3]}\n")

    return agenda  # Devolde a agenda ordena para a main
