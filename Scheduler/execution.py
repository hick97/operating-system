import numpy as np
from process import Process
import sys
import re

class Execution:
#Variaveis
    def __init__(self, tempoTotal, n_processos):
        self.lista_processos = []
        self.n_processos = n_processos
        self.fila_prontos = []
        self.tempoTotal = tempoTotal
        self.toExecutando = False
        self.regulaRR = 0
#Get e sets
    def get_nprocessos(self):
        return self.n_processos
#Append process
    def appendProcesso(self, tC, tD):
        processo = Process(tC, tD)
        self.lista_processos.append(processo)
#Execucao
    def executaFCFS(self):
        time = 0
        while(time <= self.tempoTotal):
            self.FCFS(time)
            time += 1
        tempos = self.calc_tempos()
        return tempos

    def executaSJF(self):
        time = 0
        while(time <= self.tempoTotal):
            self.SJF(time)
            time += 1
        tempos = self.calc_tempos()
        return tempos

    def executaRR(self):
        time = 0
        while(time <= self.tempoTotal):
            self.RR(time)
            time += 1
        tempos = self.calc_tempos()
        return tempos

    def FCFS(self, tAtual):

        for index, processo in enumerate(self.lista_processos):
            if(tAtual == processo.get_tChegada()):
                self.fila_prontos.append(processo)

        if(len(self.fila_prontos) != 0):
            if(self.fila_prontos[0].get_tDuracao() != 0):
                self.fila_prontos[0].set_tempos(tAtual)
                self.fila_prontos[0].set_tDuracao(self.fila_prontos[0].get_tDuracao()-1)
            else:
                self.fila_prontos[0].set_tTerminou(tAtual)
                self.fila_prontos.pop(0)
                if(len(self.fila_prontos) != 0):
                    self.fila_prontos[0].set_tempos(tAtual)
                    self.fila_prontos[0].set_tDuracao(self.fila_prontos[0].get_tDuracao()-1)

            for index, processo in enumerate(self.fila_prontos):
                if(index != 0):
                    processo.set_tFilaProntos(processo.get_tFilaProntos()+1)

    def SJF(self, tAtual):
        toPronto = 0
        for index, processo in enumerate(self.lista_processos):
            if(tAtual == processo.get_tChegada()):
                self.fila_prontos.append(processo)
                toPronto +=1

        #Ordena caso: tiver mais de 1 processo entrando no mesmo tempo && Nenhum processo tiver sendo executado
        if((toPronto > 1) and (self.toExecutando == False)):
            self.fila_prontos = sorted(self.fila_prontos, key = Process.get_tDuracao)


        if(len(self.fila_prontos) != 0):
            self.toExecutando = True
            if(self.fila_prontos[0].get_tDuracao() != 0):
                self.emExecucao = True
                self.fila_prontos[0].set_tempos(tAtual)
                self.fila_prontos[0].set_tDuracao(self.fila_prontos[0].get_tDuracao()-1)
            else:
                self.fila_prontos[0].set_tTerminou(tAtual)
                self.fila_prontos.pop(0)
                #Ordena quando um determinado processo sai
                self.fila_prontos = sorted(self.fila_prontos, key = Process.get_tDuracao)
                if(len(self.fila_prontos) != 0):
                    self.fila_prontos[0].set_tempos(tAtual)
                    self.fila_prontos[0].set_tDuracao(self.fila_prontos[0].get_tDuracao()-1)

            for index, processo in enumerate(self.fila_prontos):
                if(index != 0):
                    processo.set_tFilaProntos(processo.get_tFilaProntos()+1)
        else:
            self.toExecutando = False

    def RR(self, tAtual):

        for index, processo in enumerate(self.lista_processos):
            if(tAtual == processo.get_tChegada()):
                self.fila_prontos.append(processo)

        if(len(self.fila_prontos) != 0):
            if(self.regulaRR == 2 and self.fila_prontos[0].get_tDuracao() != 0):
                processo = self.fila_prontos.pop(0)
                self.fila_prontos.append(processo)
                self.regulaRR = 0
                self.fila_prontos[0].set_tempos(tAtual)
                self.fila_prontos[0].set_tDuracao(self.fila_prontos[0].get_tDuracao()-1)
                self.regulaRR += 1
            else:
                if(self.fila_prontos[0].get_tDuracao() != 0):
                    self.regulaRR += 1
                    self.fila_prontos[0].set_tempos(tAtual)
                    self.fila_prontos[0].set_tDuracao(self.fila_prontos[0].get_tDuracao()-1)
                else:
                    self.fila_prontos[0].set_tTerminou(tAtual)
                    self.fila_prontos.pop(0)
                    self.regulaRR = 0
                    if(len(self.fila_prontos) != 0):
                        self.fila_prontos[0].set_tempos(tAtual)
                        self.fila_prontos[0].set_tDuracao(self.fila_prontos[0].get_tDuracao()-1)
                        self.regulaRR += 1 

            for index, processo in enumerate(self.fila_prontos):
                if(index != 0):
                    processo.set_tFilaProntos(processo.get_tFilaProntos()+1)
#Calcula tempos
    def calc_tempos(self):
        Tretorno = 0
        Tresposta = 0
        Tespera = 0
        tempos = []

        for processo in self.lista_processos:
            Tretorno += processo.calc_tRetorno()
            Tresposta += processo.calc_tResposta()
            Tespera += processo.get_tFilaProntos()

        np = float(self.get_nprocessos())
        tRetornoTotal = round(float(Tretorno/np), 1)
        tRespostaTotal = round(float(Tresposta/np), 1)
        tEsperaTotal = round(float(Tespera/np), 1)

        tempos.append(tRetornoTotal)
        tempos.append(tRespostaTotal)
        tempos.append(tEsperaTotal)

        return tempos

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python execution.py entrada.txt')
        sys.exit(1)

    tTotal = 0
    lista_dados = []
    n_process = 0
#Leitura
    arq = open(sys.argv[1], 'r')
    texto = arq.readlines()
    for linha in texto:
        n_process += 1
        process = (linha.split(" "))
        lista_dados.append(process)
        time_process = re.sub('[^0-9]', '', process[1])
        tTotal += int(time_process)
    arq.close()
#Executando politicas
    exeFCFS = Execution(tTotal, n_process)
    exeSJF = Execution(tTotal, n_process)
    exeRR = Execution(tTotal, n_process)
    for index, valor in enumerate(lista_dados):
        t_chegada = int(valor[0])
        t_duracao = int(re.sub('[^0-9]', '', valor[1]))
        exeFCFS.appendProcesso(t_chegada, t_duracao)
        exeSJF.appendProcesso(t_chegada, t_duracao)
        exeRR.appendProcesso(t_chegada, t_duracao)
#Recolhendo tempos
    timeFCFS = exeFCFS.executaFCFS()
    timeSJF = exeSJF.executaSJF()
    timeRR = exeRR.executaRR()
#Escrita
    arq = open('saida.txt', 'w')
    texto = []
    texto.append('FCFS '+str(timeFCFS[0])+' '+str(timeFCFS[1]) + ' ' + str(timeFCFS[2])+'\n')
    texto.append('SJF '+str(timeSJF[0])+' '+str(timeSJF[1]) + ' ' + str(timeSJF[2])+'\n')
    texto.append('RR '+str(timeRR[0])+' '+str(timeRR[1]) + ' ' + str(timeRR[2]))
    arq.writelines(texto)
    arq.close()        
