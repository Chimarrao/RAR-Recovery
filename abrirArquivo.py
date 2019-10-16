import os
import easygui

class abrir():
    def __init__(self, labelNome, labelTamanho):
        self.labelNome                      = labelNome
        self.labelTamanho                   = labelTamanho
        self.caminhoArquivo                 = ""
        self.formatoArquivo                 = ""
    
    def run(self):
        try:
            self.caminhoArquivo             = easygui.fileopenbox(default="*.rar", filetypes=["*.zip", "*.rar"])
            self.formatoArquivo             = self.caminhoArquivo.split(".")[-1]
        
            #Coloca o nome na tela
            nome                            = self.caminhoArquivo.split("\\")
            nome                            = nome[len(nome)-1]
            self.labelNome.setText(nome)

            #Coloca o tamanho do label
            tamanhoArquivo = os.path.getsize(self.caminhoArquivo)
            #Em bytes
            if tamanhoArquivo < 1024:
                self.labelTamanho.setText(str(round(tamanhoArquivo)) + " bytes")
            #Em kilobytes
            if tamanhoArquivo > 1024 and tamanhoArquivo < 1048576:
                self.labelTamanho.setText(str(round(tamanhoArquivo/1024)) + " Kb")
            #Em megabytes
            if tamanhoArquivo > 1048576 and tamanhoArquivo < 1073741824:
                self.labelTamanho.setText(str(round((tamanhoArquivo/1024)/1024)) + " Mb")
            #Em gigabytes
            if tamanhoArquivo > 1073741824 and tamanhoArquivo < 1099511627776:
                self.labelTamanho.setText(str(round((tamanhoArquivo/1024)/1024/1024)) + " Gb")
        except:
            self.labelNome.setText("")
            self.labelTamanho.setText("")