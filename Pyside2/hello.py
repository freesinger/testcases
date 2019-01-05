from PySide2.QtWidgets import QApplication, QLabel

app = QApplication([])
lable = QLabel('<font color=blue size=50>Hello Qt for Python!</font>')
lable.show()
app.exec_()