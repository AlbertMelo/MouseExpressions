# -*- coding: utf-8 -*-
import pyautogui as pyg
import os
import subprocess
import programa

class Mouse(object):


	def __init__(self, QuadroXI, QuadroYI, Dimensao):
		self.TEMPO = 0
		
		#Touchpad do monitor
		self.QuadroXI = QuadroXI - Dimensao
		self.QuadroYI = QuadroYI - Dimensao + int(Dimensao/3)
		self.QuadroXF = QuadroXI + Dimensao
		self.QuadroYF = QuadroYI + Dimensao - int(Dimensao/3)
		self.PESODESLOCAMENTO = 1
		self.DESLOCAMENTO = 3
		self.DIMENSAO = Dimensao
		

		#precisa carregara essa configuração do arquivo de setup
		#emocoes = ['Raiva', 'Desgosto', 'Medo', 'Felicidade', 'Tristeza', 'Surpresa', 'Neutro']
		#	0:Raiva		
		#	1:Desgosto
		# 	2:Medo		
		# 	3:Felicidade
		# 	4:Tristeza
		# 	5:Supresa
		# 	6:Neutro
		
		self.comandos = { 
			'0': self.click,
			'1': self.duplo_click,
			'2': self.rolar_pagina_cima,
			'3': self.rolar_pagina_baixo,
			'4': self.sem_acao,
			'5': self.click_direito,
			'6': self.executar_arquivo
			}
	
	
	def setPesoDeslocamento(self,peso):
		self.PESODESLOCAMENTO = peso
	
	#click, duplo_click, rolar_pagina_cima, rolar_pagina_baixo, sem_acao, click_direito, atalho_alt_f4
	#Metodos de comando gerados pelo mouse

	def click(self):
		pyg.click()
		
	def duplo_click(self):
		pyg.doubleClick()

	def rolar_pagina_cima(self):
		pyg.scroll(10)

	def rolar_pagina_baixo(self):
		pyg.scroll(-10)
		
	def sem_acao(self):
		return

	def click_direito(self):
		pyg.rightClick()

	def executar_arquivo(self):
		wConfigura = programa.programaT(1, "setConfiguracoes", 2)
		wConfigura.start()
		return wConfigura

	
	#Metodos de Movimentacao do Ponteiro do Mouse

	def move_mouse_direita(self):
		pyg.moveRel(-self.DESLOCAMENTO, None, self.TEMPO)

	def move_mouse_esquerda(self):
		pyg.moveRel(self.DESLOCAMENTO, None, self.TEMPO)

	def move_mouseX(self, dx):
		pyg.moveRel(dx, None, self.TEMPO)

	def move_mouse_cima(self):
		pyg.moveRel(None, self.DESLOCAMENTO, self.TEMPO)

	def move_mouse_baixo(self):
		pyg.moveRel(None, -self.DESLOCAMENTO, self.TEMPO)

	def move_mouseY(self, dy):
		pyg.moveRel(None, dy, self.TEMPO)

	def move_mouseXY(self, dx, dy):
		pyg.moveRel(dx, dy)


	#Objetivo:  
	# Movimentar o ponteiro do mouse de acordo com o movimento da cabeça (melhor trocar para o olho). 

	def move_mouse(self, xi, yi, x, y):
		dx = x -xi
		dy = y -yi

		if abs(dx)>=self.DIMENSAO:
			 dx *= 2
		
		if abs(dy)>=self.DIMENSAO:
			 dx *= 2

		self.move_mouseXY(-dx,dy)


	def move_mouse_peso(self, xi, yi, x, y):

		dx = x - xi
		if dx<0:
			dx = dx + self.DIMENSAO
		else:
			dx = dx - self.DIMENSAO


		#Fora do quadro no eixo X
		if not (x in range(self.QuadroXI, self.QuadroXF)):
			#pyg.moveRel((x - xi - self.DIMENSAO)*-2, None, self.TEMPO)
			pyg.moveRel(dx*-2, None, self.TEMPO)

		
		
		dy = y - yi
		if dy<0:
			dy = dy + int (self.DIMENSAO/3)
		else:
			dy = dy - int (self.DIMENSAO/3)

		#Fora do quadro no eixo Y

		if not (y in range(self.QuadroYI, self.QuadroYF)):
			#pyg.moveRel(None, (y-yi-self.DIMENSAO)*2, self.TEMPO)
			pyg.moveRel(None, dy*2, self.TEMPO)
			
		'''
		if not ((x in range (self.QuadroXI,self.QuadroXF)) and (y in range (self.QuadroYI,self.QuadroYF))):
			self.move_mouse(xi, yi, x-self.DIMENSAO, y-self.DIMENSAO)
		'''

	def emularComandosMouse(self, acao):
		self.comandos[acao]()
		