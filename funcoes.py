import os
import geradorSenhas
import cracker
import easygui
import time
from PyQt5 import QtCore

def abrir(labelNome, labelTamanho):
    try:
        global nomeArquivo
        global formatoArquivo
        nomeArquivo = easygui.fileopenbox(default="*.rar", filetypes=["*.zip", "*.rar"])
        #Pega o formato do arquivo
        formatoArquivo = nomeArquivo.split(".")[-1]

        #Coloca o nome na tela
        nome = nomeArquivo.split("\\")
        nome = nome[len(nome)-1]
        labelNome.setText(nome)
        
        #Coloca o tamanho do arquivo em Kb
        if os.path.getsize(nomeArquivo) > 1024 and os.path.getsize(nomeArquivo) < 1048576:
            labelTamanho.setText(str(int(os.path.getsize(nomeArquivo)/1024)) + " Kb")
        #Coloca o tamanho do arquivo em Mb
        if os.path.getsize(nomeArquivo) > 1048576 and os.path.getsize(nomeArquivo) < 1073741824:
            labelTamanho.setText(str((int(os.path.getsize(nomeArquivo)/1024)/1024)) + " Mb")

    except Exception as e:
        print("Erro ao abrir arquivo !", e)

class iniciar(QtCore.QThread):
    sinal = QtCore.pyqtSignal(object, int)

    def __init__(self, pushButtonIniciar, progressBarProgressoGeral, tabWidget, textEditConsole, LimiteMinimo, 
            LimiteMaximo, caracteres):
        QtCore.QThread.__init__(self)
        self.pushButtonIniciar = pushButtonIniciar
        self.progressBarProgressoGeral = progressBarProgressoGeral
        self.tabWidget = tabWidget
        self.textEditConsole = textEditConsole
        self.LimiteMinimo = LimiteMinimo
        self.LimiteMaximo = LimiteMaximo
        self.caracteres = caracteres

    def run(self):
        try:
            listaSenhas = []
            inicio = 0
            tentativas = 0

            senhafoiencontrada = False
            self.sinal.emit("bloquear", 0)

            #Trocar para as variáveis da gui
            tempoInicio = time.time()
            for i in range(self.LimiteMinimo, self.LimiteMaximo+1):
                listaSenhas = geradorSenhas.gerador(listaSenhas, self.caracteres, i)
                for listaSenhas in listaSenhas:
                    tentativas += 1
                    fim = len(listaSenhas)
                    senhafoiencontrada = cracker.cracker(nomeArquivo, formatoArquivo, listaSenhas, inicio, 
                        fim, tentativas, self.textEditConsole, self.sinal, tempoInicio)
                                            
                    inicio = fim

                    if senhafoiencontrada:
                        self.sinal.emit("liberar", 0)
                        return
                    
            if not senhafoiencontrada:
                self.sinal.emit("liberar", 0)
                self.sinal.emit("apagar", 0)
                self.textEditConsole.insertPlainText("-----------------------------Senha não encontrada, tente outra configuração-----------------------------")

        except Exception as e:
            print("Erro !", e)

    def stop(self):
        self.terminate()