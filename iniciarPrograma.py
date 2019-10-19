import time
import cracker
import rarfile
import zipfile
from PyQt5 import QtCore

class iniciar(QtCore.QThread):
    sinal = QtCore.pyqtSignal(object, str)

    def __init__(self, abrir, pushButtonIniciar, progressBarProgressoGeral, tabWidget, LimiteMinimo, 
                 LimiteMaximo, caracteres, numeroThreads):
        QtCore.QThread.__init__(self)
        self.abrir                          = abrir
        self.pushButtonIniciar              = pushButtonIniciar
        self.progressBarProgressoGeral      = progressBarProgressoGeral
        self.tabWidget                      = tabWidget
        self.LimiteMinimo                   = LimiteMinimo
        self.LimiteMaximo                   = LimiteMaximo
        self.caracteres                     = caracteres
        self.numeroThreads                  = numeroThreads

    def run(self):
        #Verificações
        if self.LimiteMinimo > self.LimiteMaximo:
            self.sinal.emit("msgerro", "Limite mínimo não pode ser maior que o limite máximo")
            return
        
        if self.abrir.formatoArquivo != "zip" and self.abrir.formatoArquivo != "rar":
            self.sinal.emit("msgerro", "Arquivo inválido")
            return

        if len(self.caracteres) == 0:
            self.sinal.emit("msgerro", "Nenhum grupo de caracteres selecionado")
            return

        try:
            self.sinal.emit("bloquear", "0")

            #Criação do arquivo e envio para o cracker
            if self.abrir.formatoArquivo == "zip":
                arquivoZip = zipfile.ZipFile(self.abrir.caminhoArquivo, "r")
                senhaEncontrada = cracker.iniciar(arquivoZip, self.LimiteMinimo, self.LimiteMaximo, self.caracteres,
                                                  self.sinal, self.abrir.formatoArquivo, self.numeroThreads)
                
            if self.abrir.formatoArquivo == "rar":
                arquivoRar = rarfile.RarFile(self.abrir.caminhoArquivo, "r")
                senhaEncontrada = cracker.iniciar(arquivoRar, self.LimiteMinimo, self.LimiteMaximo, self.caracteres,
                                                  self.sinal, self.abrir.formatoArquivo, self.numeroThreads)
                                            
            #Tratamento de resultados
            if senhaEncontrada:
                self.sinal.emit("liberar", "0")
                return
            else:
                self.sinal.emit("msgatencao", "A senha não foi encontrada, tente outra configuração")
                self.sinal.emit("liberar", "0")
            
        except Exception as e:
            self.sinal.emit("msgerro", str(e))
            self.sinal.emit("liberar", "0")

    def stop(self):
        self.terminate()