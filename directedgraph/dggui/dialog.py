from PySide6.QtWidgets import (
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QDialog,
    QLabel,
    QMessageBox,
)


class InputDialogNode(QDialog):
    def __init__(self, parent=None):
        super(InputDialogNode, self).__init__(parent)
        self.setWindowTitle("Please Input Source Node Value")
        self.edit = QLineEdit(self)
        self.edit.placeholderText()
        self.button = QPushButton("Confirm")
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.confirm)

    def confirm(self):
        try:
            return float(self.edit.text())
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("You have to enter a number!!")
            msg.show()
            msg.exec_()
            return


class InputDialogArc(QDialog):
    def __init__(self, parent=None):
        super(InputDialogArc, self).__init__(parent)
        self.setWindowTitle("Please Input Linked Nodes UID")
        Label = QLabel("Arc attribute")
        self.edit1 = QLineEdit(self)
        self.edit1.setPlaceholderText("name")
        self.edit2 = QLineEdit(self)
        self.edit2.setPlaceholderText("uid1")
        self.edit3 = QLineEdit(self)
        self.edit3.setPlaceholderText("uid2")
        self.edit4 = QLineEdit(self)
        self.edit4.setPlaceholderText("user_define_arc_type")
        self.edit5 = QLineEdit(self)
        self.edit5.setPlaceholderText("user_define_attribute")
        self.button = QPushButton("Confirm")
        layout = QVBoxLayout()
        layout.addWidget(Label)
        layout.addWidget(self.edit1)
        layout.addWidget(self.edit2)
        layout.addWidget(self.edit3)
        layout.addWidget(self.edit4)
        layout.addWidget(self.edit5)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.resize(300, 100)
        self.button.clicked.connect(self.confirm)

    def confirm(self):
        return (
            self.edit1.text(),
            self.edit2.text(),
            self.edit3.text(),
            self.edit4.text(),
            self.edit5.text(),
        )
