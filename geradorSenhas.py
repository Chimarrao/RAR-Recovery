def gerador(listaSenhas, caracteres, tamanho):
    #Chave recebe o tamanho maximo da senha
    chave = []
    for i in range(0, tamanho):
        chave.append(0)

    #Arranjo com repetição
    combPossiveis = (len(caracteres) ** tamanho)

    #Cria senhas até o limite(ex: entrada: "a" "b" "c" 3 - saida: "aaa" até ""ccc"")
    for i in range(int(combPossiveis)):
        formaSenha = ""
        for i in range(0, tamanho):
            formaSenha = formaSenha + str(caracteres[chave[i]])

        listaSenhas.append(formaSenha)

        charAjuste = len(chave) - 1
        ajusteChave(chave, charAjuste, len(caracteres) - 1)
        yield listaSenhas

#Faz o ajuste da chave de senhas -> caracteres(1, 4, 5) -> (1, 4, 6)
def ajusteChave(chave, charAjuste, caracterMaior):
    if chave[charAjuste] == caracterMaior:
        chave[charAjuste] = 0
        ajusteChave(chave, charAjuste - 1, caracterMaior)
    else:
        chave[charAjuste] = chave[charAjuste] + 1