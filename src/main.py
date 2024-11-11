from src.diagnostico import *

def main():

    opcao = seleciona_opcao()

    if(int(opcao) == 1):
        modo_diagnostico()


def seleciona_opcao():
    print("Seja Bem-Vindo ao nosso Sistema de Saúde! Favor selecionar uma opção:")
    print("1. Modo diagnostico")
    print("2. Modo perguntas gerais")
    print("3. Marcar consulta");

    opcao = input("Digite a opção selecionada: ")

    while(int(opcao) < 1 or int(opcao) > 3):
        print("Opção inválida! Tente novamente")
        opcao = input("Digite a opção selecionada: ")
    
    return opcao

if __name__ == "__main__":
    main()