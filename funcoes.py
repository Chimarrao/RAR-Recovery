from PyQt5 import QtCore
import os
import geradorSenhas
import cracker
import easygui
import time

class abrir():
    def __init__(self, labelNome, labelTamanho):
        self.labelNome                      = labelNome
        self.labelTamanho                   = labelTamanho
        self.arquivoAberto                  = False
        self.caminhoArquivo                 = ""
        self.formatoArquivo                 = ""
    
    def run(self):
        try:
            self.caminhoArquivo             = easygui.fileopenbox(default="*.rar", filetypes=["*.zip", "*.rar"])
            self.formatoArquivo             = self.caminhoArquivo.split(".")[-1]
        
            #Coloca o nome na tela
            nome                            = self.caminhoArquivo.split("\\")
            nome                            = nome[len(nome)-1]
            self.labelNome.setText(nome)

            #Coloca o tamanho do arquivo em bytes
            if os.path.getsize(self.caminhoArquivo) < 1024:
                self.labelTamanho.setText(str(os.path.getsize(self.caminhoArquivo)) + " bytes")
            #Coloca o tamanho do arquivo em Kb
            if os.path.getsize(self.caminhoArquivo) > 1024 and os.path.getsize(self.caminhoArquivo) < 1048576:
                self.labelTamanho.setText(str(os.path.getsize(self.caminhoArquivo)/1024) + " Kb")
            #Coloca o tamanho do arquivo em Mb
            if os.path.getsize(self.caminhoArquivo) > 1048576 and os.path.getsize(self.caminhoArquivo) < 1073741824:
                self.labelTamanho.setText(str((os.path.getsize(self.caminhoArquivo)/1024)/1024) + " Mb")
        except:
            self.labelNome.setText("")
            self.labelTamanho.setText("")

class iniciar(QtCore.QThread):
    sinal = QtCore.pyqtSignal(object, str)

    def __init__(self, abrir, pushButtonIniciar, progressBarProgressoGeral, tabWidget, textEditConsole, LimiteMinimo, 
                 LimiteMaximo, caracteres):
        QtCore.QThread.__init__(self)

        self.abrir                          = abrir
        self.pushButtonIniciar              = pushButtonIniciar
        self.progressBarProgressoGeral      = progressBarProgressoGeral
        self.tabWidget                      = tabWidget
        self.textEditConsole                = textEditConsole
        self.LimiteMinimo                   = LimiteMinimo
        self.LimiteMaximo                   = LimiteMaximo
        self.caracteres                     = caracteres

    def run(self):
        if self.abrir.formatoArquivo != "zip" and self.abrir.formatoArquivo != "rar" or self.LimiteMinimo > self.LimiteMaximo:
            if self.LimiteMinimo > self.LimiteMaximo:
                self.sinal.emit("msgerro", "Limite mínimo não pode ser maior que o limite máximo")
            else:
                print(self.abrir.formatoArquivo)
                self.sinal.emit("msgerro", "Arquivo inválido")
        else:
            try:
                tentativas                  = 0
                listaSenhas                 = []
                combPossiveis               = 0
                numCaracteres               = len(self.caracteres)
                tempoInicio                 = time.time()

                for tamanho in range(self.LimiteMinimo, self.LimiteMaximo+1):
                    combPossiveis = combPossiveis + (numCaracteres ** tamanho)
            
                parte                       = combPossiveis/100
                senhaEncontrada             = False

                self.sinal.emit("bloquear", "0")
                for i in range(self.LimiteMinimo, self.LimiteMaximo+1):
                    listaSenhas = geradorSenhas.gerador(listaSenhas, self.caracteres, i)
                
                    for listaSenhas in listaSenhas:
                        #Alimentar a lista de senhas antes de passar pro cracker
                        tentativas          += 1
                        fim                 = len(listaSenhas)
                        senhaEncontrada     = cracker.cracker(self.abrir.caminhoArquivo, self.abrir.formatoArquivo, listaSenhas, i,
                                                              self.caracteres, fim, tentativas, self.textEditConsole,
                                                              self.sinal, tempoInicio, parte)
                                            
                        i = fim

                        if senhaEncontrada:
                            self.sinal.emit("liberar", "0")
                            return
                    
                if not senhaEncontrada:
                    self.sinal.emit("msginformacao", "A senha não foi encontrada, tente outra configuração")
                    self.sinal.emit("liberar", "0")

            except Exception as e:
                self.sinal.emit("msgerro", str(e))

    def stop(self):
        self.terminate()