from src.ia import *

class Diagnostico:
    def __init__(self, *sintomas):
        self.__sintomas = sintomas

    def getSintomas(self):
        return self.__sintomas

    def avaliarSintomas(self):
        ia = Ia()

        configuracao = (
            "Você é uma inteligência artificial especializada em diagnósticos médicos. " +
            "Quando um usuário fornecer uma lista de sintomas, responda apenas com um possível diagnóstico e uma forma de tratamento. " +
            "Não forneça quaisquer outras informações, mesmo relacionado a medicina, ou converse assuntos além do diagnóstico relacionado aos sintomas fornecidos. " +
            "Caso não seja fornecida uma lista de sintomas, informe que não poderá realizar o diagnostico e nada além disso"
        )

        sintomas_texto = ", ".join(self.__sintomas)

        resposta = ia.responder_pergunta_unica(configuracao, sintomas_texto)

        return resposta

def efetuar_diagnostico(sintomas):
    sintomas = sintomas.split(",")
    diagnostico = Diagnostico(*sintomas)
    return diagnostico.avaliarSintomas()

