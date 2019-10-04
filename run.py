import sys
import gui
from PyQt5 import QtWidgets

#Criação da janela
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    janela = QtWidgets.QMainWindow()
    ui = gui.Ui_janela()
    ui.setupUi(janela)
    janela.show()
    sys.exit(app.exec_())