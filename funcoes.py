import os
import geradorSenhas
import cracker
import easygui
import time
from PyQt5 import QtCore

def abrir(labelNome, labelTamanho):
    try:
        global caminhoArquivo
        global formatoArquivo
        caminhoArquivo                      = easygui.fileopenbox(default="*.rar", filetypes=["*.zip", "*.rar"])
        formatoArquivo                      = caminhoArquivo.split(".")[-1]

        #Coloca o nome na tela
        nome                                = caminhoArquivo.split("\\")
        nome                                = nome[len(nome)-1]
        labelNome.setText(nome)

        #Coloca o tamanho do arquivo em bytes
        if os.path.getsize(caminhoArquivo) < 1024:
            labelTamanho.setText(str(int(os.path.getsize(caminhoArquivo))) + " bytes")
        #Coloca o tamanho do arquivo em Kb
        if os.path.getsize(caminhoArquivo) > 1024 and os.path.getsize(caminhoArquivo) < 1048576:
            labelTamanho.setText(str(int(os.path.getsize(caminhoArquivo)/1024)) + " Kb")
        #Coloca o tamanho do arquivo em Mb
        if os.path.getsize(caminhoArquivo) > 1048576 and os.path.getsize(caminhoArquivo) < 1073741824:
            labelTamanho.setText(str((int(os.path.getsize(caminhoArquivo)/1024)/1024)) + " Mb")

    except Exception as e:
        print("Erro ao abrir arquivo !", e)

class iniciar(QtCore.QThread):
    sinal = QtCore.pyqtSignal(object, int)

    def __init__(self, pushButtonIniciar, progressBarProgressoGeral, tabWidget, textEditConsole, LimiteMinimo, 
                 LimiteMaximo, caracteres):
        QtCore.QThread.__init__(self)
        self.pushButtonIniciar              = pushButtonIniciar
        self.progressBarProgressoGeral      = progressBarProgressoGeral
        self.tabWidget                      = tabWidget
        self.textEditConsole                = textEditConsole
        self.LimiteMinimo                   = LimiteMinimo
        self.LimiteMaximo                   = LimiteMaximo
        self.caracteres                     = caracteres

    def run(self):
        try:
            i                               = 0
            tentativas                      = 0
            listaSenhas                     = []
            combPossiveis                   = 0
            numCaracteres                   = len(self.caracteres)
            tempoInicio                     = time.time()

            for tamanho in range(self.LimiteMinimo, self.LimiteMaximo+1):
                combPossiveis = combPossiveis + (numCaracteres ** tamanho)
            
            parte                           = combPossiveis/100
            senhafoiencontrada              = False

            self.sinal.emit("bloquear", 0)
            #Trocar para as variáveis da gui
            for i in range(self.LimiteMinimo, self.LimiteMaximo+1):
                listaSenhas                 = geradorSenhas.gerador(listaSenhas, self.caracteres, i)
                
                for listaSenhas in listaSenhas:
                    tentativas              += 1
                    fim                     = len(listaSenhas)
                    senhafoiencontrada      = cracker.cracker(caminhoArquivo, formatoArquivo, listaSenhas, i,
                                                              self.caracteres, fim, tentativas, self.textEditConsole,
                                                              self.sinal, tempoInicio, parte)
                                            
                    i = fim

                    if senhafoiencontrada:
                        self.sinal.emit("liberar", 0)
                        return
                    
            if not senhafoiencontrada:
                self.sinal.emit("liberar", 0)
                self.textEditConsole.insertPlainText("-----------------------------Senha não encontrada, tente outra configuração-----------------------------")

        except Exception as e:
            print("Erro !", e)

    def stop(self):
        self.terminate()