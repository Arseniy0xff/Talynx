from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QDialog, QLabel, QListWidgetItem

from functional_module import FuncMod
from ui_py.DialogNoteViewAndEdit import Ui_Dialog

import name_space

class DialogNoteViewAndEdit(QDialog):
    openItemBySuggestion = pyqtSignal(str, list)
    def __init__(self, text='', tags=[], notes_dict={}):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(str(name_space.ICON_PATH)))

        self.ui.textEdit.setFont(QFont(name_space.FONT_FAMALY, name_space.FONT_SIZE + name_space.FONT_SIZE_FORM_TEXT_SHIFT))
        self.ui.plainTextEdit.setFont(QFont(name_space.FONT_FAMALY, name_space.FONT_SIZE + name_space.FONT_SIZE_FORM_TEXT_SHIFT))

        self.text = text
        self.tags = tags
        self.notes_dict = notes_dict

        self.ui.listWidget.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.ui.textEdit.setText(text)
        self.ui.plainTextEdit.setPlainText(' '.join(tags))

        self.generate_suggestions()


    def generate_suggestions(self):

        for i in self.filter_by_tags(self.tags):

            item = (QListWidgetItem
                    (FuncMod().str_lim(i['text'], name_space.TEXT_LIMIT_ON_SUGGESTIONS_BY_TAGS))
                    )

            only_match = ', '.join(list(set(i['tags']) & set(self.tags)))
            residue = ', '.join(list(set(i['tags']) - set(self.tags)))
            only_match += f' ({residue})' if len(residue) > 0 else ''

            item.setToolTip(only_match)
            item.setData(Qt.ItemDataRole.UserRole, i)
            self.ui.listWidget.addItem(item)


    def filter_by_tags(self, required_tags: list) -> list:
        matches = []
        for item in self.notes_dict['content']:
            if item['text'] == self.text:
                continue
            item_tags = set(item.get("tags", []))
            common = item_tags.intersection(required_tags)
            if common:
                matches.append((len(common), item))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in matches]


    def on_item_double_clicked(self, item: QListWidgetItem):
        stored_dict = item.data(Qt.ItemDataRole.UserRole)
        self.openItemBySuggestion.emit(stored_dict['text'], stored_dict['tags'])


    def get_clean_tags(self) -> list:
        return [p.strip() for  p in self.ui.plainTextEdit.toPlainText().split() if p.strip()]