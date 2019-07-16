import threading
import os, subprocess

class programaT(threading.Thread):
    def __init__(self, threadID, nome, contador):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.nome = nome
        self.contador = contador

    def run(self):
        subprocess.call(['python','configuracoes.py'])
        