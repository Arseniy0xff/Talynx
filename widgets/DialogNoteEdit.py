from PyQt6.QtWidgets import QDialog
from ui_py.DialogNoteEdit import Ui_Dialog

class DialogNoteEdit(QDialog):
    def __init__(self, text='', tags=[]):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.textEdit.setFocus()

        self.ui.textEdit.setText(text)
        if len(tags) > 0:
            self.ui.lineEdit.setText(' '.join(tags))


