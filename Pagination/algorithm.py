import numpy as np
import sys
import re

class Algorithm:
	def __init__(self, nQuadros, referencia_pagina):
		self.referencia_pagina = referencia_pagina
		self.nQuadros = nQuadros
		self.ram_frames = []*nQuadros
		self.nFaltas = 0

	def FIFO(self):
		frame_atual = 0
		for index, pagina in enumerate(self.referencia_pagina):
			if(len(self.ram_frames) < self.nQuadros):
				if(self.ram_frames.count(pagina) == 0):
					self.ram_frames.append(pagina)
					self.nFaltas += 1
			else:
				if(self.ram_frames.count(pagina) == 0):
					self.ram_frames.pop(frame_atual)
					self.ram_frames.insert(frame_atual,pagina)
					self.nFaltas += 1
					if(frame_atual < self.nQuadros-1):
						frame_atual += 1
					else:
						frame_atual = 0
		return self.nFaltas

	def maior_periodo(self, pos_page, ram_frames, FLAG):
		sublist = []
		indices = []

		if FLAG == 0:
			for pagina in (self.referencia_pagina[pos_page:]):
				sublist.append(pagina)
		else:
			for pagina in (self.referencia_pagina[:pos_page]):
				sublist.append(pagina)
			sublist.reverse()	
		for index, valor in enumerate(ram_frames):
			if(sublist.count(valor) > 0):
				indices.append(sublist.index(valor))
			else:
				return index

		indice_maior = ram_frames.index(sublist[max(indices)])

		return indice_maior

	def OTM(self):
		for index, pagina in enumerate(self.referencia_pagina):
			if(len(self.ram_frames) < self.nQuadros):
				if(self.ram_frames.count(pagina) == 0):
					self.ram_frames.append(pagina)
					self.nFaltas += 1
			else:
				if(self.ram_frames.count(pagina) == 0):
					maior = self.maior_periodo(index+1, self.ram_frames, 0)
					self.ram_frames.pop(int(maior))
					self.ram_frames.insert(int(maior), pagina)
					self.nFaltas += 1

		return self.nFaltas

	def LRU(self):
		for index, pagina in enumerate(self.referencia_pagina):
			if(len(self.ram_frames) < self.nQuadros):
				if(self.ram_frames.count(pagina) == 0):
					self.ram_frames.append(pagina)
					self.nFaltas += 1
			else:
				if(self.ram_frames.count(pagina) == 0):
					maior = self.maior_periodo(index, self.ram_frames, 1)
					self.ram_frames.pop(int(maior))
					self.ram_frames.insert(int(maior), pagina)
					self.nFaltas += 1

		return self.nFaltas

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print('Usage: python algorithm.py entrada.txt')
		sys.exit(1)
	
	number_frames = 0
	reference_pages = []

	arq = open(sys.argv[1], 'r')
	texto = arq.readlines()
	for index, linha in enumerate(texto):
		if(index == 0):
			number_frames = re.sub('[^0-9]', '', linha)
		else:
			pagina = re.sub('[^0-9]', '', linha)
			reference_pages.append(pagina)

	FIFO = Algorithm(int(number_frames), reference_pages)
	OTM = Algorithm(int(number_frames), reference_pages)
	LRU = Algorithm(int(number_frames), reference_pages)

	faltasFIFO = FIFO.FIFO()
	faltasOTM = OTM.OTM()
	faltasLRU = LRU.LRU()

	print('FIFO ' + str(faltasFIFO))
	print('OTM ' + str(faltasOTM))
	print('LRU ' + str(faltasLRU))					
