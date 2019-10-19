import time
import rarfile
import zipfile
import patoolib
import geradorSenhas
from threading import Thread

rarfile.UNRAR_TOOL = "UnRAR.exe"

def iniciar(arquivo, LimiteMinimo, LimiteMaximo, caracteres, sinal, formatoArquivo, numeroThreads):
    parte                                   = 0
    chave                                   = 0
    tentativas                              = 0
    listaSenhas                             = []
    threads                                 = []
    tempoInicio                             = time.time()
    global                                  senhaEncontrada
    senhaEncontrada                         = False

    #Pega 1% das combinações, para a barra de progresso
    for tamanho in range(LimiteMinimo, LimiteMaximo+1):
        parte = parte + (len(caracteres) ** tamanho)
            
    parte = parte/100

    #Roda o programa do limite mínimo ao máximo
    for i in range(LimiteMinimo, LimiteMaximo+1):
        gerador = geradorSenhas.gerador(listaSenhas, caracteres, i)               
        for listaSenhas in gerador:
            tentativas += 1

            if senhaEncontrada:
                return True
            
            #Apaga o console
            if tentativas % 10 == 0:
                sinal.emit("apagar", "0")

            #Atualiza a barra de progresso
            percentual = -1
            if int(tentativas/parte) > percentual:
                percentual = int(tentativas/parte)
                sinal.emit("atualizarBarra", str(percentual))

            #Atualiza a velocidade do cracker
            diferencaEmSegundos = time.time()-tempoInicio
            if diferencaEmSegundos < 1:
                velocidade = 0
            else:
                velocidade = tentativas/diferencaEmSegundos

            #Printa as atualizações do programa no console
            conteudo = "Senha atual: {} - Velocidade média: {} senhas p/ seg\r".format(listaSenhas[-1], int(velocidade))
            sinal.emit("console", conteudo)
            
            #Cria threads
            thread = Thread(target = cracker, args = (arquivo, formatoArquivo, sinal, listaSenhas[-1], tentativas))
            threads.append(thread)
            thread.start()

            #Limita a criação de Threads
            if len(threads) >= int(numeroThreads):
                threads[chave].join()
                chave += 1

    return False

def cracker(arquivo, formatoArquivo, sinal, senha,tentativas):
    try:
        if formatoArquivo == "zip":
            arquivo.extractall(path = "./Arquivos extraídos/", pwd = str.encode(senha))
                
        if formatoArquivo == "rar":
            arquivo.extractall(path = "./Arquivos extraídos/", pwd = senha)
        
        global senhaEncontrada
        senhaEncontrada = True

        conteudo = "Arquivo extraído ! \nSenhas testadas: {} \nSenha do arquivo: {}".format(tentativas, senha)
        
        sinal.emit("apagar", "0")
        sinal.emit("console", conteudo)
        sinal.emit("msginformacao", conteudo)
        return
    except:
        pass