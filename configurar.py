# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QLayout
from PyQt5 import QtGui
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMessageBox
from configurar_ui import Ui_configurarWindow
import configuracoes as cfg 
import sys
 
class configurarWindow(QDialog):
 
    def __init__(self):
    
        super(configurarWindow, self).__init__()
        
        self.ui = Ui_configurarWindow()
        self.ui.setupUi(self)
        self.ui.btSalvar.clicked.connect(lambda:self.SalvarOnClick())
        self.ui.btCancelar.clicked.connect(lambda:self.CancelarOnClick())
        expressoes = cfg.lerArquivoExpressoes()
        self.ui.cbCliqueSimples.addItems(expressoes)
        self.ui.cbCliqueDuplo.addItems(expressoes)
        self.ui.cbRolarCima.addItems(expressoes)
        self.ui.cbRolarBaixo.addItems(expressoes)
        self.ui.cbNenhumaAcao.addItems(expressoes)
        self.ui.cbCliqueInverso.addItems(expressoes)
        self.ui.cbTeclaAtalho.addItems(expressoes)

        set_atual = cfg.lerArquivoConfiguracoes()

        self.ui.cbCliqueSimples.setCurrentIndex(int(set_atual[0]))
        self.ui.cbCliqueDuplo.setCurrentIndex(int(set_atual[1]))
        self.ui.cbRolarCima.setCurrentIndex(int(set_atual[2]))
        self.ui.cbRolarBaixo.setCurrentIndex(int(set_atual[3]))
        self.ui.cbNenhumaAcao.setCurrentIndex(int(set_atual[4]))
        self.ui.cbCliqueInverso.setCurrentIndex(int(set_atual[5]))
        self.ui.cbTeclaAtalho.setCurrentIndex(int(set_atual[6]))

    def SalvarOnClick(self):
        strnovosetup=""
        strnovosetup += str(self.ui.cbCliqueSimples.currentIndex()) + ";"
        strnovosetup += str(self.ui.cbCliqueDuplo.currentIndex()) + ";"
        strnovosetup += str(self.ui.cbRolarCima.currentIndex()) + ";"
        strnovosetup += str(self.ui.cbRolarBaixo.currentIndex()) + ";"
        strnovosetup += str(self.ui.cbNenhumaAcao.currentIndex()) + ";"
        strnovosetup += str(self.ui.cbCliqueInverso.currentIndex()) + ";"
        strnovosetup += str(self.ui.cbTeclaAtalho.currentIndex()) + ";"
        cfg.gravarArquivoConfiguracoes(strnovosetup)
        QMessageBox.information(self, "Mensagem", "Configurações registradas! É necessário re-iniciar o programa!",QMessageBox.Ok)
        app.exit()
    
    def CancelarOnClick(self):
        QMessageBox.information(self, "Mensagem", "Nenhuma alteração realizada!",QMessageBox.Ok)
        app.exit()
 
if __name__ == "__main__":
    app=QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window=configurarWindow()
    window.setWindowTitle("Protótipo - MouseExpressions - Configurações do Aplicativo")
    window.setFixedSize(window.size())
    window.show()
    sys.exit(app.exec_())