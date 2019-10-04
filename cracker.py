import rarfile
import zipfile
import time

rarfile.UNRAR_TOOL = "UnRAR.exe"

def cracker(nomeArquivo, formatoArquivo, listaSenhas, inicio, fim, tentativas, textEditConsole, sinal, tempoInicio):
    if formatoArquivo == "zip":
        arquivoZip = zipfile.ZipFile(nomeArquivo, "r")
    elif formatoArquivo == "rar":
        arquivoRar = rarfile.RarFile(nomeArquivo, "r")
    
    for indice in range(inicio, len(listaSenhas)):
        tentativas += 1
        
        #Apaga o console
        if tentativas % 10 == 0:
            sinal.emit("apagar", 0)
            
        #Atualiza a barra de progresso
        tempoAtual = time.time()
        diferencaEmSegundos = time.time()-tempoInicio
        if diferencaEmSegundos < 1:
            senhasPSeg = 0
        else:
            senhasPSeg = tentativas/ diferencaEmSegundos

        textEditConsole.insertPlainText("Senha atual: {} - Velocidade média: {} senhas p/ seg\r".format(listaSenhas[indice], int(senhasPSeg)))
        sinal.emit("atualizarBarra", tentativas)
        try:
            if formatoArquivo == "zip":
                arquivoZip.extractall(path = "./Arquivo extraídos", pwd = str.encode(listaSenhas[indice]))
            elif formatoArquivo == "rar":
                arquivoRar.extractall(path = "./Arquivo extraídos", pwd = listaSenhas[indice])
            
            textEditConsole.insertPlainText("---------------------------------------------Arquivo extraido------------------------------------------------\r")
            textEditConsole.insertPlainText("Senhas testadas: {}\r".format(tentativas))
            textEditConsole.insertPlainText("A senha é: {}\r".format(listaSenhas[indice]))

            return True
        except:
            pass
    return False