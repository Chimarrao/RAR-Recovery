import time
import rarfile
import zipfile
import patoolib
import threading
import geradorSenhas
from threading import Thread

rarfile.UNRAR_TOOL = "UnRAR.exe"

class cracker():
    def __init__(self, arquivo, LimiteMinimo, LimiteMaximo, caracteres, sinal, formatoArquivo, numeroThreads,
                posSenhaInic):
        self.arquivo                        = arquivo
        self.LimiteMinimo                   = LimiteMinimo
        self.LimiteMaximo                   = LimiteMaximo
        self.caracteres                     = caracteres
        self.sinal                          = sinal
        self.formatoArquivo                 = formatoArquivo
        self.numeroThreads                  = numeroThreads
        self.posSenhaInic                   = posSenhaInic
    
    def run(self):
        parte                               = 0
        chave                               = 0
        tentativas                          = 0
        listaSenhas                         = []
        threads                             = []
        tempoInicio                         = time.time()
        global                              senhaEncontrada
        senhaEncontrada                     = False

        #Pega 1% das combinações, para a barra de progresso
        for tamanho in range(self.LimiteMinimo, self.LimiteMaximo+1):
            parte = parte + (len(self.caracteres) ** tamanho)
            
        parte = parte/100

        #Roda o programa do limite mínimo ao máximo
        for i in range(self.LimiteMinimo, self.LimiteMaximo+1):
            gerador = geradorSenhas.gerador(listaSenhas, self.caracteres, i)               
            #Se o usuário pausar, o programa consumirá a lista até
            #a última posição +1
            for listaSenhas in gerador:
                if(len(listaSenhas) < self.posSenhaInic):
                    tentativas += 1
                    continue
                else:
                    break

            for listaSenhas in gerador:
                tentativas += 1

                if senhaEncontrada:
                    return True
            
                #Apaga o console
                if tentativas % 10 == 0:
                    self.sinal.emit("apagar", "0")

                #Atualiza a barra de progresso
                percentual = int(tentativas/parte)
                self.sinal.emit("atualizarBarra", str(percentual))

                #Atualiza a velocidade do cracker
                diferencaEmSegundos = time.time()-tempoInicio
                if diferencaEmSegundos < 1:
                    velocidade = 0
                else:
                    velocidade = tentativas/diferencaEmSegundos

                #Pega a posição da ultima senha testada
                if tentativas >= int(self.numeroThreads)+1:
                    self.sinal.emit("posiscaoUltSenha", str(tentativas-(int(self.numeroThreads)+1)))
                else:
                    self.sinal.emit("posiscaoUltSenha", str(0))

                #Printa as atualizações do programa no console
                conteudo = "Senha atual: {} - Velocidade média: {} senhas p/ seg\r".format(listaSenhas[-1], int(velocidade))
                self.sinal.emit("console", conteudo)
            
                #Cria threads
                thread = multithreading(self.formatoArquivo, self.arquivo, self.sinal, listaSenhas[-1], tentativas)
                threads.append(thread)
                thread.start()

                #Limita a criação de Threads
                if len(threads) >= int(self.numeroThreads):
                    threads[chave].join()
                    chave += 1

        return False

class multithreading(threading.Thread):
    def __init__(self, formatoArquivo, arquivo, sinal, senha, tentativas):
        threading.Thread.__init__(self)
        self.formatoArquivo                 = formatoArquivo
        self.arquivo                        = arquivo
        self.sinal                          = sinal
        self.senha                          = senha
        self.tentativas                     = tentativas

    def run(self):
        try:
            if self.formatoArquivo == "zip":
                self.arquivo.extractall(path = "./Arquivos extraídos/", pwd = str.encode(self.senha))
                
            if self.formatoArquivo == "rar":
                self.arquivo.extractall(path = "./Arquivos extraídos/", pwd = self.senha)
        
            global senhaEncontrada
            senhaEncontrada = True

            conteudo = "Arquivo extraído ! \nSenhas testadas: {} \nSenha do arquivo: {}".format(self.tentativas, self.senha)
        
            self.sinal.emit("apagar", "0")
            self.sinal.emit("console", conteudo)
            self.sinal.emit("msginformacao", conteudo)
            return
        except:
            pass