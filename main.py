import sys
from PySide2 import QtWidgets
import MainWindow

def main():
    
    app=QtWidgets.QApplication(sys.argv)
    ui=MainWindow.MainWindow()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()