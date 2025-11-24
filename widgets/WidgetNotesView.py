from PyQt6.QtWidgets import QDialog, QListWidgetItem

import name_space
from DSM import DSM
from ui_py.WidgetNotesView import Ui_Form

from widgets.DialogNoteEdit import DialogNoteEdit
from widgets.DialogNoteView import DialogNoteView
from widgets.WidgetItemCard import WidgetItemCard


class WidgetNotesView(QDialog):
    def __init__(self, notes_dict, password):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.notes_dict = notes_dict
        self.password = password
        print(f'Password: "{password}"')

        self.ui.pushButton.clicked.connect(self.new_item)
        self.ui.pushButton_2.clicked.connect(self.save_note)

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
            widget_instance.ui.pushButton.setText(text[:name_space.TEXT_LIMIT_IN_BUTTONS] + '...' if len(text) > name_space.TEXT_LIMIT_IN_BUTTONS else '')

            widget_instance.removeRequested.connect(self.remove_item)
            widget_instance.updateDictRequested.connect(self.dict_data_update)
            widget_instance.openNoteView.connect(self.note_view)

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
        for i in self.notes_dict['content']:
            self.new_item(i['text'], i['tags'], without_dialog=True)


    def note_view(self, text, tags):
        d = DialogNoteView(text, tags, self.notes_dict)
        d.exec()


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
        for k, v in unique.items():
            item = QListWidgetItem(f'{k} ({v})')
            self.ui.listWidget_2.addItem(item)


    def remove_item(self, widget):
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            if self.ui.listWidget.itemWidget(item) is widget:
                self.ui.listWidget.takeItem(i)
                widget.deleteLater()
                del item
                self.dict_data_update()
                break