# -*- coding: utf-8 -*-

PATH_COMANDOS = "setup.txt"
PATH_EXPRESSOES = "expressoes.txt"

'''
    Codigo: Expressao/Comando
    0: raiva
    1: desgosto
    2: medo
    3: felicidade
    4: tristeza
    5: surpresa
    6: neutro
    ------------------
    ordem padrao:
    0: click
    1: duplo_click
    2: rolar_pagina_cima
    3: rolar_pagina_baixo
    4: sem_acao
    5: click_contrario
    6: atalho_alt_tab
    --------------------
    expr_padrao: 5;1;3;4;6;2;0;    
'''

def lerArquivoConfiguracoes():
    SETCOMANDOS=[]
    arq = open(PATH_COMANDOS, "r")

    for linha in arq:
        SETCOMANDOS = linha.split(';')
    SETCOMANDOS.pop()   
    
    arq.close()
    
    return SETCOMANDOS

def gravarArquivoConfiguracoes(NOVOSCOMANDOS):
    try:
        arq = open(PATH_COMANDOS, "w")
        arq.write(NOVOSCOMANDOS)
        arq.close()
    except:
        print("Erro: não foi possível gravar as configurações!")

def lerArquivoExpressoes():
    SETEXPRESSOES=[]
    arq = open(PATH_EXPRESSOES, "r")

    for linha in arq:
        SETEXPRESSOES = linha.split(';')
    SETEXPRESSOES.pop()   
    
    arq.close()
    
    return SETEXPRESSOES

def gravarArquivoExpressoes(NOVASEXPRESSOES):

    arq = open(PATH_EXPRESSOES, "w")
    STR_GRAVAR = ""
    
    for i in range(len(NOVASEXPRESSOES)):
        STR_GRAVAR+= NOVASEXPRESSOES[i] + ";"

    arq.write(str(STR_GRAVAR))
    arq.close()