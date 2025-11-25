import sys
from pathlib import Path


def resource_path(relative_path: str) -> Path:
    base_path = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent
    return base_path / relative_path

ICON_PATH = resource_path('icons/icon.ico')
PATH_TO_NOTES = Path('data/')
if not PATH_TO_NOTES.is_dir():
    PATH_TO_NOTES.mkdir(parents=True, exist_ok=True)

TEXT_LIMIT_ON_SUGGESTIONS_BY_TAGS = 20
TEXT_LIMIT_IN_BUTTONS = 14

TAG_HIDING_SYMBOL = '_'

FONT_FAMALY = 'Open Sans'
FONT_SIZE = 9
FONT_SIZE_FORM_TEXT_SHIFT = 1
