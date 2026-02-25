from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel
from NetGarden.GUI.i18n import tr

class SavedPacketsWindow(QWidget):
    def __init__(self, lang, get_saved_packets, on_jump):
        super().__init__()
        self.lang = lang
        self.get_saved_packets = get_saved_packets
        self.on_jump = on_jump

        self.resize(560, 420)

        layout = QVBoxLayout()
        self.hint = QLabel()
        layout.addWidget(self.hint)

        self.list = QListWidget()
        self.list.itemClicked.connect(self._clicked)
        layout.addWidget(self.list)

        self.setLayout(layout)
        self.apply_lang()
        self.refresh()

    def apply_lang(self):
        self.setWindowTitle(tr(self.lang, "saved_title"))
        self.hint.setText(tr(self.lang, "saved_hint"))

    def refresh(self):
        self.list.clear()
        saved = self.get_saved_packets()
        for s in saved:
            self.list.addItem(f"[{s['timestamp']}] {s['direction']} | {s['id']}")

    def _clicked(self, item):
        idx = self.list.row(item)
        self.on_jump(idx)