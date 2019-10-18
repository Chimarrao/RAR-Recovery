import time
import rarfile
import zipfile
import patoolib
import geradorSenhas

rarfile.UNRAR_TOOL = "UnRAR.exe"

def cracker(arquivo, LimiteMinimo, LimiteMaximo, caracteres, sinal, formatoArquivo):
    parte                                   = 0
    tentativas                              = 0
    listaSenhas                             = []
    tempoInicio                             = time.time()

    #Pega 1% das combinações, para a barra de progresso
    for tamanho in range(LimiteMinimo, LimiteMaximo+1):
        parte = parte + (len(caracteres) ** tamanho)
            
    parte = parte/100
    
    #Roda o programa do limite mínimo ao máximo
    for i in range(LimiteMinimo, LimiteMaximo+1):
        gerador = geradorSenhas.gerador(listaSenhas, caracteres, i)               
        for listaSenhas in gerador:
            tentativas += 1

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

            sinal.emit("console", "Senha atual: {} - Velocidade média: {} senhas p/ seg\r".format(
                        listaSenhas[-1], int(velocidade)))
            try:
                if formatoArquivo == "zip":
                    arquivo.extractall(path = "./Arquivo extraídos", pwd = str.encode(listaSenhas[-1]))
                
                if formatoArquivo == "rar":
                    arquivo.extractall(path = "./Arquivo extraídos", pwd = listaSenhas[-1])

                sinal.emit("msginformacao", "Arquivo extraído ! \nSenhas testadas: {} \nSenha do arquivo: {}".format(
                            tentativas, listaSenhas[-1]))
                return True
            except:
                pass
    return False
