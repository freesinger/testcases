from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout

class Form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set window name
        self.setWindowTitle("Write your name")
        # Create widgets
        self.edit = QLineEdit()
        self.button = QPushButton("Show Greetings")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)

    # Greet user in console
    def greetings(self):
        print("づ￣3￣）づ╭❤～ {}".format(self.edit.text()))

    
if __name__ == '__main__':
    app = QApplication([])
    # Create and show the form
    form = Form()
    form.show()
    app.exec_()