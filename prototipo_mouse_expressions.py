# -*- coding: utf-8 -*-
import numpy as np
import cv2 as cv
from keras.preprocessing import image
from keras.models import model_from_json
import click
import pandas as pd
from keras.layers import Input
from keras import models
from keras.models import load_model
import pyautogui
import statistics
from PyQt5 import QtWidgets, QtGui
from configurar import configurarWindow
import sys
import configuracoes as cfg 
import camera
import mouse 
import teclado
import matplotlib.pyplot as plt

pyautogui.FAILSAFE = False

class mouse_expressions(object):

	def __init__(self):
		#Constantes de controle
		#comandos: [click, duplo_click, rolar_pagina_cima, rolar_pagina_baixo, sem_acao, click_contrario, atalho_alt_tab]
		#emocoes = ['Raiva', 'Desgosto', 'Medo', 'Felicidade', 'Tristeza', 'Surpresa', 'Neutro']
		self.emocoes = ["raiva", "desgosto", "medo", "felicidade", "tristeza", "surpresa", "neutro"]
		self.FRAMES_VELOCIDADE = 30

		#Carregando as configuracoes
		self.FACES_CALIBRAGEM = 20
		self.LOTE_IMAGENS = 15
		self.SEQUENCIA_EXPRESSOES = []
		self.DIMENSAO = 30
		
		#Definicoes dos arquivso externos de configuracao
		self.PATH_MODEL = "./model/modelo_cnn_major_20_10.h5"
		self.PATH_SETUP = "setup.txt"

		print("Carregando arquivos:\n")
		
		#Carrega modelos do OpenCV para detectar
		#FACE
		self.face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_alt.xml")
		
		print("- modelos do OpenCV")
		#	Carregando  modelos de aprendidos CNN
		print("- -  compilando modelo \n")
		self.model = load_model(self.PATH_MODEL)
		self.model.compile
		
		print("- arquivo de configurações")
		self.COMANDOS = cfg.lerArquivoConfiguracoes()
		print(self.COMANDOS)
		
		
		#Instanciando Camera
		self.camera = camera.Camera()
		if camera != None:
			(self.xi_cabeca, self.yi_cabeca) = self._calibra_posicao_inicial_cabeca(camera, self.FACES_CALIBRAGEM)

		#Instanciando Mouse
		self.mouse = mouse.Mouse(
			self.xi_cabeca,
			self.yi_cabeca,
			self.DIMENSAO)

		#Instanciando Teclado
		self.teclado = teclado.Teclado()
		

	#Captura um posicao padrao da cabeca para que possa 
	#fazer o deslocamento do mouse
	#ponto de referencia 				#melhorar
	def _calibra_posicao_inicial_cabeca(self, camera, FACES_CALIBRAGEM):

		print("Inicio Calibragem da posicao de cabeca")

		acx = 0
		acy = 0
		xi = -1000
		xy = -1000
		conta_faces = 0

		for i in range(FACES_CALIBRAGEM):
			ref, img = self.camera.lerImagem()
			if ref:
				frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
				face = self.face_cascade.detectMultiScale(frame, 1.3, 5) #detecta o rosto
				if len(face)>0:
					for (xf,yf,hf,wf) in face:
						acx += xf
						acy += yf
						conta_faces += 1

			#cv.imshow('Calibrando posição cabeça',img)


		if conta_faces>0:
			xi = int(acx/conta_faces)
			yi = int(acy/conta_faces)
		else:
			print("Não foi possível detectar rosto! Erro de calibragem")
			camera.pararCaptura()
			cv.destroyAllWindows()
			exit()

		print("Fim calibragem!")
		print("posicao", xi , yi)
		
		return (xi, yi)
	
	#trata imagem da face e faz a predicao
	def _classificarExpressao(self, img,frame, x, y, w, h):

		#trata imagem
		cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #retangulo na face
		cv.rectangle(img,(self.xi_cabeca-self.DIMENSAO,
							self.yi_cabeca-self.DIMENSAO + int(self.DIMENSAO/3)),
							(self.xi_cabeca+self.DIMENSAO,
							self.yi_cabeca+self.DIMENSAO-+ int(self.DIMENSAO/3)),
							(0,255,0),1)
							
		detected_face = frame[int(y):int(y+h), int(x):int(x+w)] #recorta face detectada
		detected_face = cv.resize(detected_face,(48, 48))#redimensiona imagem para 48x48
		
		#trata imagem do rosto para classificar a expressao
		rosto = image.img_to_array(detected_face)
		rosto = np.expand_dims(rosto, axis = 0)
		rosto /= 255. #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]
		rosto = rosto.reshape(-1, 48, 48, 1)

		#predição da expressão do rosto de acordo com o modelo treinado
		expressao = self.model.predict(rosto)

		return np.argmax(expressao)


	#Objetivo: Reconhecer expressões faciais e posição da cabeça 
	# em quadro extraído do vídeo recebido de uma chamada de rotina.

	def _reconhecerExpressoesFaciais(self, img, frame, face, xi_cabeca, yi_cabeca):
		
		for (x,y,w,h) in face: #detectar faces que esta em primeiro plano (trabalhos futuros)
			#detecta a expressao do usuario
			expressao = self._classificarExpressao(img, frame, x, y, w, h)
			return(expressao)	
			
			                                                                                                                                                                                                                                                                                   
	#-----------------------------		
	#Objetivo: Determinar a partir de informações fornecidas pelo UC 001 se 
	# ocorreu alguma intenção de ação por parte dos usuários a partir do quadro extraído do vídeo capturado pela webcam. 
	#Realiza emulacao de comando que está associada a expressao
	def _classificarExpressaoAcao(self, expressao):

		#array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
		
		for i in range(len(self.COMANDOS)):
			if int(self.COMANDOS[i]) == expressao:
				self.mouse.emularComandosMouse(str(i))


	#-----------------------------
	#Objetivo: Identificar a ocorrência de expressões faciais e 
	# movimentos realizados com a cabeça utilizando imagens de vídeos capturadas pela webcam. 

	def _analisaOcorrenciaAcoesUsuario(self, img, frame, face, xi_cabeca, yi_cabeca):
		
		moda = self.COMANDOS[4]
		#movimentacao mecanica do mouse (a intecao de movimentar deve ser incluida em trabalhos futuros)
		for (x,y,h,w) in face: # aprimorar para considerar apenas quem esta em frente ao equipamento (reconhecer o usuário)
			expressao = self._reconhecerExpressoesFaciais(img, frame, face, xi_cabeca, yi_cabeca)
			self.SEQUENCIA_EXPRESSOES.append(expressao)
			
			if (len(self.SEQUENCIA_EXPRESSOES)>=self.LOTE_IMAGENS):
				try:
					moda = int(statistics.mode(self.SEQUENCIA_EXPRESSOES))
				except:
					moda = int(self.COMANDOS[4]) #padrao sem acao *****************************falta ajustar pra ser o valor da acao que naum executa nenhuma acao
				
				expressao = moda 
				#Emula o comando
				self._classificarExpressaoAcao(moda) 
				self.SEQUENCIA_EXPRESSOES = []
					
		return expressao	
			
	def executar(self):
			
		while(True):
			#padrao de comando para não executar comandos
			expressao=int(self.COMANDOS[4])  #comando 4 é padrao para naum realizar tarefa
			ref, img = self.camera.lerImagem()
			if ref: #leu imagem
				frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
				face = self.face_cascade.detectMultiScale(frame, 1.3, 5) #detecta os rostos no frame
				if len(face)>0:
					(x, y, h, w) = face[0]
					#movimenta ponteiro mouse
					self.mouse.move_mouse_peso(self.xi_cabeca,self.yi_cabeca,x, y)
					#anlisa expressao
					expressao = self._analisaOcorrenciaAcoesUsuario(img, frame, face, self.xi_cabeca,self.yi_cabeca)

			cv.putText(img, self.emocoes[expressao], (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 0), 3, cv.LINE_AA)
			cv.imshow('img',img)
			#encerra loop/programa
			key = cv.waitKey(1)
			if  key==27: #press Esc para encerrar
				break

		#finaliza objetos do OpenCV
		self.camera.pararCaptura()
		cv.destroyAllWindows()
		exit()

if __name__== '__main__':
	mouse_expressions().executar()