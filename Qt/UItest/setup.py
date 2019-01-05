from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

class MainWindow(QMainWindow):
    def __init__(self):
        # python 2
        # super(MainWindow, self).__init__()
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication([])
    # from ui_mainwindow import Ui_MainWindow
    # window = MainWindow()
    # window.show()
    # app.exec_()

    ui_file = QFile('mainwindow.ui')
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    window.show()

    app.exec_()