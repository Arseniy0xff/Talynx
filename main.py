import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QDialog

from DSM import DSM
from ui_py.MainWindow import Ui_MainWindow
from widgets.DialogNoteSetting import DialogNoteSetting
from widgets.WidgetNoteCard import WidgetNoteCard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.create_new_note)
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.DSM = DSM()
        self.load_notes()
        # print(self.DSM.get_all_notes())


    def create_new_note(self, notes_dict = None):
        try:
            password = ''
            if not notes_dict:
                dialog_new_note = DialogNoteSetting()
                if dialog_new_note.exec() == QDialog.DialogCode.Accepted:
                    notes_dict = {}
                    notes_dict['name'] = dialog_new_note.ui.lineEdit.text()
                    notes_dict['file_name'] = self.DSM.generate_filename()
                    notes_dict['encrypt'] = True if dialog_new_note.ui.lineEdit_2.text() else False
                    notes_dict['ofi'] = 0
                    notes_dict['content'] = dict()
                    password = dialog_new_note.ui.lineEdit_2.text()

                else:
                    return


            widget_instance = WidgetNoteCard(self, notes_dict, password)
            widget_instance.ui.label.setText(notes_dict['name'])
            # widget_instance.removeRequested.connect(self.remove_custom_item)
            list_item = QListWidgetItem()
            list_item.setSizeHint(widget_instance.sizeHint())

            self.ui.listWidget.addItem(list_item)
            self.ui.listWidget.setItemWidget(list_item, widget_instance)
            self.ui.listWidget.scrollToItem(list_item)


        except Exception as e:
            print(e)

    def load_notes(self):
        [self.create_new_note(_) for _ in self.DSM.get_all_notes()]

    def close_tab(self, index):
        widget = self.ui.tabWidget.widget(index)
        self.ui.tabWidget.removeTab(index)
        widget.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
