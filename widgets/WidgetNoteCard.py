from PyQt6.QtWidgets import QDialog, QMessageBox, QWidget
from ui_py.WidgetNoteCard import Ui_Form

from widgets.WidgetNotesView import WidgetNotesView
from widgets.DialogEnterPassword import DialogEnterPassword
from widgets.DialogNoteSetting import DialogNoteSetting

class WidgetNoteCard(QWidget):
    def __init__(self, parent, notes_dict: dict, password = ''):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.notes_dict = notes_dict
        self.parent = parent
        self.password = password

        self.ui.toolButton.clicked.connect(self.open_settings)
        self.ui.pushButton.clicked.connect(self.open_note)


    def open_settings(self):
        if self.notes_dict["encrypt"] and not self.password:
            if not self.pass_request():
                return

        dialog_new_note = DialogNoteSetting()
        dialog_new_note.ui.lineEdit.setText(self.notes_dict['name'])
        dialog_new_note.ui.lineEdit_2.setText(self.password)
        dialog_new_note.ui.lineEdit_3.setText(self.password)

        if dialog_new_note.exec() == QDialog.DialogCode.Accepted:
            self.notes_dict['name'] = dialog_new_note.ui.lineEdit.text()
            self.notes_dict['encrypt'] = True if dialog_new_note.ui.lineEdit_2.text() else False
            self.password = dialog_new_note.ui.lineEdit_2.text()
            self.parent.DSM.save_dict_to_json(self.notes_dict, self.password)


    def open_note(self):
        if self.notes_dict["encrypt"] and not self.password:
            if not self.pass_request():
                return

        w = WidgetNotesView(self.notes_dict, self.password)
        self.parent.ui.tabWidget.addTab(w, self.notes_dict['name'])
        self.parent.ui.tabWidget.setCurrentIndex(self.parent.ui.tabWidget.count() - 1)


    def pass_request(self):
        dialog_pass = DialogEnterPassword()
        if dialog_pass.exec() == QDialog.DialogCode.Accepted:
            self.password = dialog_pass.ui.lineEdit.text()
            d = self.notes_dict
            # decrypt
            if len(self.password) > 0:
                try:
                    d = self.parent.DSM.decrypt_dict(self.notes_dict, self.password)
                except Exception as e:
                    print(e)

            if isinstance(d['content'], list):
                self.notes_dict = d
                return True
            else:
                dlg = QMessageBox(self)
                dlg.setIcon(QMessageBox.Icon.Critical)
                dlg.setWindowTitle('Error')
                dlg.setText('Wrong Password')
                dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
                dlg.exec()
                self.password = ''
        return False