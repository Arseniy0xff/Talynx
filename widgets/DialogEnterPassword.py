from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLineEdit, QDialogButtonBox
from ui_py.DialogEnterPassword import Ui_Dialog

class DialogEnterPassword(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.lineEdit.setFocus()
        self.ui.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)

        self.ui.checkBox.stateChanged.connect(self.switch_mode_entred_pass)
        # self.ui.lineEdit.textChanged.connect(self.password_correct)
        # self.ui.lineEdit_2.textChanged.connect(self.password_correct)
        # self.ui.checkBox.stateChanged.connect(self.password_correct)

        # self.ok_btn = self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok)
        self.ui.lineEdit_2.hide()


    def switch_mode_entred_pass(self, state):
        if state == Qt.CheckState.Checked.value:
            self.ui.lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
            # self.ui.lineEdit_2.hide()
        else:
            self.ui.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
            # self.ui.lineEdit_2.show()

    # def password_correct(self):
    #     if self.ui.lineEdit.text() == self.ui.lineEdit_2.text() or self.ui.checkBox.checkState() == Qt.CheckState.Checked:
    #         self.ok_btn.setEnabled(True)
    #     else:
    #         self.ok_btn.setEnabled(False)
