from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QDialog

from functional_module import FuncMod
from ui_py.WidgetItemCard import Ui_Form
from widgets.DialogNoteEdit import DialogNoteEdit
from widgets.DialogNoteViewAndEdit import DialogNoteViewAndEdit

import name_space


class WidgetItemCard(QWidget):

    removeRequested = pyqtSignal(QWidget)
    viewAndEditRequested = pyqtSignal(QWidget)
    updateDictRequested = pyqtSignal()
    openNoteView = pyqtSignal(str, list)

    def __init__(self, text='', tags=[]):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.ui.toolButton.setIcon(QIcon("icons/sliders_icon-icons.com_67990.svg"))
        # self.ui.toolButton_2.setIcon(QIcon("icons/trash_bin_icon-icons.com_67981.svg"))

        self.ui.pushButton.clicked.connect(self.view_and_edit_item)
        # self.ui.toolButton.clicked.connect(self.edit_item)
        self.ui.toolButton_2.clicked.connect(self.on_delete_clicked)

        self.text = text
        self.tags = tags


    def view_item(self):
        self.openNoteView.emit(self.text, self.tags)

    def edit_item(self):
        d = DialogNoteEdit(self.text, self.tags)
        d.exec()

        self.text = d.ui.textEdit.toPlainText()
        self.tags = d.ui.lineEdit.text().split() if len(d.ui.lineEdit.text()) > 0 else []

        self.ui.pushButton.setText(
            FuncMod().str_lim(self.text, name_space.TEXT_LIMIT_IN_BUTTONS)
        )

        self.updateDictRequested.emit()


    def view_and_edit_item(self):
        self.viewAndEditRequested.emit(self)


    def on_delete_clicked(self):
        self.removeRequested.emit(self)