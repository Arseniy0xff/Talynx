from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from ui_py.WidgetItemCard import Ui_Form


class WidgetItemCard(QWidget):

    removeRequested = pyqtSignal(QWidget)
    viewAndEditRequested = pyqtSignal(QWidget)

    def __init__(self, text='', tags=[]):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.ui.toolButton.setIcon(QIcon("icons/sliders_icon-icons.com_67990.svg"))
        # self.ui.toolButton_2.setIcon(QIcon("icons/trash_bin_icon-icons.com_67981.svg"))

        self.ui.pushButton.clicked.connect(self.view_and_edit_item)
        self.ui.toolButton_2.clicked.connect(self.on_delete_clicked)

        self.text = text
        self.tags = tags


    def view_and_edit_item(self):
        self.viewAndEditRequested.emit(self)

    def on_delete_clicked(self):
        self.removeRequested.emit(self)