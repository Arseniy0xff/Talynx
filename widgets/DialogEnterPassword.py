from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QLineEdit, QDialogButtonBox

import name_space
from ui_py.DialogEnterPassword import Ui_Dialog

class DialogEnterPassword(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(str(name_space.ICON_PATH)))

        self.ui.lineEdit.setFocus()
        self.ui.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)

        self.ui.checkBox.stateChanged.connect(self.switch_mode_entred_pass)
        self.ui.lineEdit_2.hide()

    def switch_mode_entred_pass(self, state):
        if state == Qt.CheckState.Checked.value:
            self.ui.lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
