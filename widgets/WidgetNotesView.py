from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QListWidgetItem, QWidget

import name_space
from DSM import DSM
from functional_module import FuncMod
from ui_py.WidgetNotesView import Ui_Form

from widgets.DialogNoteEdit import DialogNoteEdit
from widgets.DialogNoteViewAndEdit import DialogNoteViewAndEdit
from widgets.WidgetItemCard import WidgetItemCard


class WidgetNotesView(QWidget):
    def __init__(self, notes_dict, password):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(str(name_space.ICON_PATH)))

        self.notes_dict = notes_dict
        self.password = password
        # print(f'Password: "{password}"')

        self.ui.pushButton.clicked.connect(self.new_item)
        self.ui.pushButton_2.clicked.connect(self.save_note)
        self.ui.listWidget_2.itemSelectionChanged.connect(self.display_items_only_selected_tags)
        self.ui.lineEdit.textChanged.connect(self.display_items_only_search)

        self.DSM = DSM()

        self.load_items_from_dict()
        try:
            self.show_all_tags()
        except Exception as e:
            print(e)


    def new_item(self, text='', tags=[], without_dialog=False):
        try:
            if not without_dialog:
                d = DialogNoteEdit()
                d.exec()

                text = d.ui.textEdit.toPlainText()
                tags = d.ui.lineEdit.text().split() if len(d.ui.lineEdit.text()) > 0 else []

            widget_instance = WidgetItemCard(text, tags)

            widget_instance.ui.pushButton.setText(
                FuncMod().str_lim(text, name_space.TEXT_LIMIT_IN_BUTTONS)
            )

            widget_instance.removeRequested.connect(self.remove_item)
            widget_instance.viewAndEditRequested.connect(self.view_and_edit_item)

            list_item = QListWidgetItem()
            list_item.setSizeHint(widget_instance.sizeHint())

            self.ui.listWidget.addItem(list_item)
            self.ui.listWidget.setItemWidget(list_item, widget_instance)
            self.ui.listWidget.scrollToItem(list_item)

            self.dict_data_update()

        except Exception as e:
            print(e)


    def save_note(self):
        self.DSM.save_dict_to_json(self.notes_dict, self.password)


    def load_items_from_dict(self):
        self.ui.listWidget.clear()
        for i in self.notes_dict['content']:
            self.new_item(i['text'], i['tags'], without_dialog=True)


    def view_and_edit_item(self, widget):
        try:
            d = DialogNoteViewAndEdit(widget.text, widget.tags, self.notes_dict)
            d.openItemBySuggestion.connect(self.open_item_by_suggestion)

            if d.exec() == QDialog.DialogCode.Accepted:
                widget.text = d.ui.textEdit.toPlainText()
                widget.tags = d.ui.plainTextEdit.toPlainText().split() if len(d.ui.plainTextEdit.toPlainText()) > 0 else []

                widget.ui.pushButton.setText(
                    FuncMod().str_lim(widget.text, name_space.TEXT_LIMIT_IN_BUTTONS)
                )

                self.dict_data_update()
        except Exception as e:
            print(e)

    def open_item_by_suggestion(self, text, tags):
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            if self.ui.listWidget.itemWidget(item).text == text and self.ui.listWidget.itemWidget(item).tags == tags:
                self.ui.listWidget.itemWidget(item).view_and_edit_item()
                break


    def dict_data_update(self):
        self.notes_dict['content'] = []
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            widget_class = self.ui.listWidget.itemWidget(item)

            self.notes_dict['content'].append({
                "text": widget_class.text,
                "tags": widget_class.tags,
            })
        self.show_all_tags()


    def show_all_tags(self):
        unique = {}

        for i in self.notes_dict['content']:
            for j in i['tags']:
                unique[j] = unique.get(j, 0) + 1

        self.ui.listWidget_2.clear()

        item = QListWidgetItem('')
        item.setData(Qt.ItemDataRole.UserRole, 'space')
        self.ui.listWidget_2.addItem(item)

        for k, v in unique.items():
            item = QListWidgetItem(f'{k} ({v})')
            item.setData(Qt.ItemDataRole.UserRole, k)
            self.ui.listWidget_2.addItem(item)


    def display_items_only_selected_tags(self):
        if len(self.ui.listWidget_2.selectedItems()) > 0:

            if len(self.ui.listWidget_2.selectedItems()) == 1:
                item = self.ui.listWidget_2.selectedItems()[0]
                if item.data(Qt.ItemDataRole.UserRole) == 'space':
                    for i in range(self.ui.listWidget.count()):
                        item = self.ui.listWidget.item(i)
                        item.setHidden(False)
                    return

            selected_tags = []
            for item in self.ui.listWidget_2.selectedItems():
                selected_tags.append(item.data(Qt.ItemDataRole.UserRole))

            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                widget_class = self.ui.listWidget.itemWidget(item)
                if len(set(widget_class.tags) & set(selected_tags)) > 0:
                    item.setHidden(False)
                else:
                    item.setHidden(True)
        else:
            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                item.setHidden(False)


    def display_items_only_search(self):
        if len(self.ui.lineEdit.text()) > 0:

            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                widget_class = self.ui.listWidget.itemWidget(item)

                if self.ui.lineEdit.text().lower() in widget_class.text.lower():
                    item.setHidden(False)
                else:
                    item.setHidden(True)

        else:
            for i in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(i)
                item.setHidden(False)


    def remove_item(self, widget):
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            if self.ui.listWidget.itemWidget(item) is widget:
                self.ui.listWidget.takeItem(i)
                widget.deleteLater()
                del item
                self.dict_data_update()
                break