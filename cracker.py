import rarfile
import zipfile
import time

rarfile.UNRAR_TOOL = "UnRAR.exe"

def cracker(caminhoArquivo, formatoArquivo, listaSenhas, inicio, caracteres, fim, tentativas,textEditConsole,
            sinal, tempoInicio, parte):
    if formatoArquivo == "zip":
        arquivoZip = zipfile.ZipFile(caminhoArquivo, "r")
    elif formatoArquivo == "rar":
        arquivoRar = rarfile.RarFile(caminhoArquivo, "r")

    for indice in range(inicio, len(listaSenhas)):
        tentativas += 1

        #Apaga o console
        if tentativas % 10 == 0:
            sinal.emit("apagar", "0")

        #Atualiza a barra de progresso
        percentual = 0
        if int(tentativas/parte) > percentual:
            percentual = int(tentativas/parte)
            sinal.emit("atualizarBarra", str(percentual))

        #Atualiza a velocidade do cracker
        diferencaEmSegundos                 = time.time()-tempoInicio

        if diferencaEmSegundos < 1:
            senhasPSeg = 0
        else:
            senhasPSeg = tentativas/diferencaEmSegundos

        textEditConsole.insertPlainText("Senha atual: {} - Velocidade média: {} senhas p/ seg\r".format(
            listaSenhas[indice], int(senhasPSeg)))
        try:
            if formatoArquivo == "zip":
                arquivoZip.extractall(path="./Arquivo extraídos", pwd = str.encode(listaSenhas[indice]))
            elif formatoArquivo == "rar":
                arquivoRar.extractall(path="./Arquivo extraídos", pwd=listaSenhas[indice])

            sinal.emit("msginformacao", "Arquivo extraído ! \nSenhas testadas: {} \nSenha do arquivo: {}".format(
                tentativas, listaSenhas[indice]))
            return True
        except:
            pass
    return False
