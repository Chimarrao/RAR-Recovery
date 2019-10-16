import time
import cracker
import rarfile
import zipfile
import geradorSenhas
from PyQt5 import QtCore

class iniciar(QtCore.QThread):
    sinal = QtCore.pyqtSignal(object, str)

    def __init__(self, abrir, pushButtonIniciar, progressBarProgressoGeral, tabWidget, LimiteMinimo, 
                 LimiteMaximo, caracteres):
        QtCore.QThread.__init__(self)
        self.abrir                          = abrir
        self.pushButtonIniciar              = pushButtonIniciar
        self.progressBarProgressoGeral      = progressBarProgressoGeral
        self.tabWidget                      = tabWidget
        self.LimiteMinimo                   = LimiteMinimo
        self.LimiteMaximo                   = LimiteMaximo
        self.caracteres                     = caracteres

    def run(self):
        if self.abrir.formatoArquivo != "zip" and self.abrir.formatoArquivo != "rar" or self.LimiteMinimo > self.LimiteMaximo:
            if self.LimiteMinimo > self.LimiteMaximo:
                self.sinal.emit("msgerro", "Limite mínimo não pode ser maior que o limite máximo")
            else:
                self.sinal.emit("msgerro", "Arquivo inválido")
        else:
            try:
                tentativas                  = 0
                combPossiveis               = 0
                listaSenhas                 = []
                senhaEncontrada             = False
                tempoInicio                 = time.time()
                numCaracteres               = len(self.caracteres)

                for tamanho in range(self.LimiteMinimo, self.LimiteMaximo+1):
                    combPossiveis = combPossiveis + (numCaracteres ** tamanho)
            
                parte = combPossiveis/100
                
                self.sinal.emit("bloquear", "0")
                
                if self.abrir.formatoArquivo == "zip":
                    arquivoZip = zipfile.ZipFile(self.abrir.caminhoArquivo, "r")
                
                if self.abrir.formatoArquivo == "rar":
                    arquivoRar = rarfile.RarFile(self.abrir.caminhoArquivo, "r")

                for i in range(self.LimiteMinimo, self.LimiteMaximo+1):
                    listaSenhas = geradorSenhas.gerador(listaSenhas, self.caracteres, i)               
                    for listaSenhas in listaSenhas:
                        tentativas          += 1
                        fim                 = len(listaSenhas)
                        
                        if self.abrir.formatoArquivo == "zip":
                            senhaEncontrada = cracker.cracker(arquivoZip, self.abrir.formatoArquivo, listaSenhas, 
                                                                  i, tentativas, self.sinal, tempoInicio, parte)
                        
                        if self.abrir.formatoArquivo == "rar":
                            senhaEncontrada = cracker.cracker(arquivoRar, self.abrir.formatoArquivo, listaSenhas, 
                                                                  i, tentativas, self.sinal, tempoInicio, parte)
                                            
                        i = fim

                        if senhaEncontrada:
                            self.sinal.emit("liberar", "0")
                            return
                    
                if not senhaEncontrada:
                    self.sinal.emit("msginformacao", "A senha não foi encontrada, tente outra configuração")
                    self.sinal.emit("liberar", "0")
            
            except Exception as e:
                self.sinal.emit("msgerro", str(e))
                self.sinal.emit("liberar", "0")

    def stop(self):
        self.terminate()