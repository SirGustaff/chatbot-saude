from src.ia import *
from src.prompts import *

class Diagnostico:
    def __init__(self, *sintomas):
        self.__sintomas = sintomas

    def getSintomas(self):
        return self.__sintomas

    def avaliarSintomas(self):
        ia = Ia()

        configuracao = diagnostico_prompt

        sintomas_texto = ", ".join(self.__sintomas)

        resposta = ia.responder_pergunta_unica(configuracao, sintomas_texto)

        return resposta

def efetuar_diagnostico(sintomas):
    sintomas = sintomas.split(",")
    diagnostico = Diagnostico(*sintomas)
    return diagnostico.avaliarSintomas()

