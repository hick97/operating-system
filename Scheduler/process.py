import numpy as np

class Process:
#Variaveis
    def __init__(self, tC, tD):
        self.toExecutando = []
        self.tChegada = tC
        self.tDuracao = tD
        self.tTerminou = 0
        self.tFilaProntos = 0
#Metodos Get e Set
    def set_tempos(self, valor):
        self.toExecutando.append(valor)

    def get_tChegada(self):
        return self.tChegada

    def get_tDuracao(self):
        return self.tDuracao

    def set_tDuracao(self, valor):
        self.tDuracao = valor

    def get_tTerminou(self):
        return self.tTerminou
    
    def set_tTerminou(self, valor):
        self.tTerminou = valor

    def get_tFilaProntos(self):
        return self.tFilaProntos
    
    def set_tFilaProntos(self, valor):
        self.tFilaProntos = valor

    def calc_tRetorno(self):
        return (self.tTerminou - self.tChegada)

    def calc_tResposta(self):
        return (self.toExecutando[0] - self.tChegada)

