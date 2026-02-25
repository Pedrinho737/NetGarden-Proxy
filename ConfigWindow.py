import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox, QComboBox
)

from NetGarden.GUI.i18n import load_settings, save_settings, tr, LANG_PT, LANG_EN

RECENTS_PATH = os.path.join(os.path.dirname(__file__), "recent.json")


def _load_recents():
    if not os.path.exists(RECENTS_PATH):
        return []
    try:
        with open(RECENTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except:
        return []


def _save_recents(items):
    try:
        with open(RECENTS_PATH, "w", encoding="utf-8") as f:
            json.dump(items[:20], f, ensure_ascii=False, indent=2)
    except:
        pass


class ConfigWindow(QWidget):
    def __init__(self, on_start, lang):
        super().__init__()
        self.on_start = on_start
        self.recents = _load_recents()
        self.lang = lang

        self.resize(820, 380)

        root = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()

        # language row
        lang_row = QHBoxLayout()
        self.lang_label = QLabel()
        self.lang_combo = QComboBox()
        self.lang_combo.addItem(tr(LANG_PT, "ptbr"), LANG_PT)
        self.lang_combo.addItem(tr(LANG_EN, "en"), LANG_EN)
        self.lang_combo.setCurrentIndex(0 if self.lang == LANG_PT else 1)
        self.lang_combo.currentIndexChanged.connect(self._on_lang_changed)
        lang_row.addWidget(self.lang_label)
        lang_row.addWidget(self.lang_combo)
        left.addLayout(lang_row)

        # fields
        self.client_ip = QLineEdit("127.0.0.1")
        self.client_port = QLineEdit("10001")

        self.server_ip = QLineEdit("127.0.0.1")
        self.server_port = QLineEdit("10001")

        row1 = QHBoxLayout()
        self.client_ip_label = QLabel()
        row1.addWidget(self.client_ip_label)
        row1.addWidget(self.client_ip)
        self.btn_local = QPushButton()
        self.btn_local.clicked.connect(lambda: self.client_ip.setText("127.0.0.1"))
        row1.addWidget(self.btn_local)

        row2 = QHBoxLayout()
        self.client_port_label = QLabel()
        row2.addWidget(self.client_port_label)
        row2.addWidget(self.client_port)

        row3 = QHBoxLayout()
        self.server_ip_label = QLabel()
        row3.addWidget(self.server_ip_label)
        row3.addWidget(self.server_ip)

        row4 = QHBoxLayout()
        self.server_port_label = QLabel()
        row4.addWidget(self.server_port_label)
        row4.addWidget(self.server_port)

        left.addSpacing(10)
        left.addLayout(row1)
        left.addLayout(row2)
        left.addSpacing(12)
        left.addLayout(row3)
        left.addLayout(row4)
        left.addSpacing(18)

        self.btn_start = QPushButton()
        self.btn_start.clicked.connect(self.start_clicked)
        left.addWidget(self.btn_start)

        # recents
        self.recents_label = QLabel()
        right.addWidget(self.recents_label)
        self.recent_list = QListWidget()
        self.recent_list.itemClicked.connect(self.pick_recent)
        right.addWidget(self.recent_list)

        self.btn_clear = QPushButton()
        self.btn_clear.clicked.connect(self.clear_recents)
        right.addWidget(self.btn_clear)

        root.addLayout(left, 2)
        root.addLayout(right, 1)
        self.setLayout(root)

        self.refresh_recents_ui()
        self.apply_lang()

    def _on_lang_changed(self):
        self.lang = self.lang_combo.currentData()
        save_settings({"lang": self.lang})
        self.apply_lang()

    def apply_lang(self):
        self.setWindowTitle(tr(self.lang, "app_launcher_title"))

        self.lang_label.setText(tr(self.lang, "language"))
        self.client_ip_label.setText(tr(self.lang, "client_ip"))
        self.client_port_label.setText(tr(self.lang, "client_port"))
        self.server_ip_label.setText(tr(self.lang, "server_ip"))
        self.server_port_label.setText(tr(self.lang, "server_port"))

        self.btn_local.setText(tr(self.lang, "local_btn"))
        self.btn_start.setText(tr(self.lang, "start_proxy"))
        self.recents_label.setText(tr(self.lang, "recents"))
        self.btn_clear.setText(tr(self.lang, "clear_recents"))

    def refresh_recents_ui(self):
        self.recent_list.clear()
        for r in self.recents:
            self.recent_list.addItem(
                f"{r['client_ip']}:{r['client_port']} → {r['server_ip']}:{r['server_port']}"
            )

    def pick_recent(self, item):
        idx = self.recent_list.row(item)
        if idx < 0 or idx >= len(self.recents):
            return
        r = self.recents[idx]
        self.client_ip.setText(r["client_ip"])
        self.client_port.setText(str(r["client_port"]))
        self.server_ip.setText(r["server_ip"])
        self.server_port.setText(str(r["server_port"]))

    def clear_recents(self):
        self.recents = []
        _save_recents(self.recents)
        self.refresh_recents_ui()

    def start_clicked(self):
        try:
            cfg = {
                "client_ip": self.client_ip.text().strip(),
                "client_port": int(self.client_port.text().strip()),
                "server_ip": self.server_ip.text().strip(),
                "server_port": int(self.server_port.text().strip()),
                "lang": self.lang
            }
        except:
            QMessageBox.warning(self, "NetGarden", tr(self.lang, "invalid_ports"))
            return

        self.recents = [r for r in self.recents if not (
            r["client_ip"] == cfg["client_ip"] and r["client_port"] == cfg["client_port"] and
            r["server_ip"] == cfg["server_ip"] and r["server_port"] == cfg["server_port"]
        )]
        self.recents.insert(0, cfg)
        _save_recents(self.recents)
        self.refresh_recents_ui()

        self.on_start(cfg)