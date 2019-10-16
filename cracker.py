import rarfile
import zipfile
import time

rarfile.UNRAR_TOOL = "UnRAR.exe"

def cracker(arquivo, formatoArquivo, listaSenhas, inicio, tentativas, sinal, tempoInicio, parte):
    for indice in range(inicio, len(listaSenhas)):
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
        diferencaEmSegundos                 = time.time()-tempoInicio
        if diferencaEmSegundos < 1:
            velocidade = 0
        else:
            velocidade = tentativas/diferencaEmSegundos

        sinal.emit("console", "Senha atual: {} - Velocidade média: {} senhas p/ seg\r".format(
                    listaSenhas[indice], int(velocidade)))
        try:
            if formatoArquivo == "zip":
                arquivo.extractall(path="./Arquivo extraídos", pwd = str.encode(listaSenhas[indice]))
            elif formatoArquivo == "rar":
                arquivo.extractall(path="./Arquivo extraídos", pwd = listaSenhas[indice])

            sinal.emit("msginformacao", "Arquivo extraído ! \nSenhas testadas: {} \nSenha do arquivo: {}".format(
                tentativas, listaSenhas[indice]))
            return True
        except:
            pass
    return False
