from src.ia import *

class Diagnostico:
    def __init__(self, *sintomas):
        self.__sintomas = sintomas

    def getSintomas(self):
        return self.__sintomas

    def avaliarSintomas(self):
        ia = Ia()

        configuracao = (
            "Você é uma inteligência artificial especializada em diagnósticos médicos. "
            
            "Quando um usuário fornecer uma lista de sintomas, responda apenas com um possível diagnóstico e uma forma de tratamento. "
            "Não forneça outras informações ou conversas além do diagnóstico relacionado aos sintomas fornecidos."
        )

        sintomas_texto = ", ".join(self.__sintomas)

        return ia.resposta(configuracao, sintomas_texto)

def modo_diagnostico():
    print("Digite os seus sintomas, cada um separado por um espaço")
    sintomas = input("Sintomas: ").split(",")

    diagnostico = Diagnostico(*sintomas)

    print(diagnostico.avaliarSintomas())

