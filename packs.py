minusculas = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

maiusculas = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

acentuadas = ["á", "é", "í", "ó", "ú", "ç", "ã", "õ", "à", "Á", "É", "Í", "Ó", "Ú", "Ç", "Ã", "Õ", "À"]

#simbolos = ["", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "=", "_", "+", "[", "]", "{", "}", "\", "|", ";", """, "'", ",", ".", "<", ">", "/", "?"]

espaco = [" "]

def retornaCaracteres(caracteres, checkBoxTodos, checkBoxLetrasMaiusculas, checkBoxLetrasMinusculas, 
                      checkBoxLetrasAcentuadas, checkBoxNumeros, checkBoxSimbolos, checkBoxEspaco):
    if checkBoxTodos.isChecked():
        caracteres.extend(maiusculas)
        caracteres.extend(minusculas)
        caracteres.extend(acentuadas)
        caracteres.extend(numeros)
        #caracteres.extend(simbolos)
        caracteres.extend(espaco)
    else:
        if checkBoxLetrasMaiusculas.isChecked():
            caracteres.extend(maiusculas)

        if checkBoxLetrasMinusculas.isChecked():
            caracteres.extend(minusculas)
        
        if checkBoxLetrasAcentuadas.isChecked():
            caracteres.extend(acentuadas)

        if checkBoxNumeros.isChecked():
            caracteres.extend(numeros)

        if checkBoxSimbolos.isChecked():
            #caracteres.extend(simbolos)
            pass

        if checkBoxEspaco.isChecked():
            caracteres.extend(espaco)

    return caracteres

def retornaNumeroCaracteres(checkBoxTodos, checkBoxLetrasMaiusculas, checkBoxLetrasMinusculas, checkBoxLetrasAcentuadas, 
                            checkBoxNumeros, checkBoxSimbolos, checkBoxEspaco): 
    contador = 0
    if checkBoxTodos.isChecked():
        contador = contador + 26
        contador = contador + 26
        contador = contador + 18
        contador = contador + 10
        #Adicionar símbolos
        contador = contador + 10
    else:
        if checkBoxLetrasMaiusculas.isChecked():
            contador = contador + 26

        if checkBoxLetrasMinusculas.isChecked():
            contador = contador + 26
        
        if checkBoxLetrasAcentuadas.isChecked():
            contador = contador + 18

        if checkBoxNumeros.isChecked():
            contador = contador + 10

        if checkBoxSimbolos.isChecked():
            #Adicionar símbolos
            pass

        if checkBoxEspaco.isChecked():
            contador = contador + 1

    return contador