import json
import datetime
from PySide6.QtWidgets import (
    QMainWindow, QListWidget, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QSplitter, QWidget, QVBoxLayout,
    QLineEdit, QLabel, QHBoxLayout, QMenu, QPushButton
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor

from NetGarden.CORE.NetStrings import NETSTRINGS
from NetGarden.GUI.i18n import tr


class MainWindow(QMainWindow):
    packet_signal = Signal(object)
    log_signal = Signal(str)

    def __init__(self, lang):
        super().__init__()
        self.lang = lang

        self.packet_counter_client = 0
        self.packet_counter_server = 0

        self.packet_colors = {}
        self.packet_items_by_id = {}
        self.filter_text = ""
        self.string_mode = False

        self.hidden_ids = set()
        self.hidden_packets = []

        self.auto_hide_spam = False
        self.spam_threshold_per_sec = 25
        self._per_id_hits = {}
        self._per_id_hits_window_ms = 1000

        self.saved_packets = []
        self.saved_window = None
        self.current_selected_packet = None

        self.packet_signal.connect(self._add_packet_safe)
        self.log_signal.connect(self._add_log_safe)

        top_bar = QHBoxLayout()
        self.filter_box = QLineEdit()
        self.filter_box.textChanged.connect(self.set_filter)

        self.options_btn = QPushButton()
        self.options_btn.clicked.connect(self.show_options_menu)

        self.stats_label = QLabel()

        top_bar.addWidget(self.filter_box)
        top_bar.addWidget(self.options_btn)
        top_bar.addWidget(self.stats_label)

        top_widget = QWidget()
        top_widget.setLayout(top_bar)

        self.client_list = QListWidget()
        self.server_list = QListWidget()

        self.client_list.itemClicked.connect(self.inspect)
        self.server_list.itemClicked.connect(self.inspect)

        self.client_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.server_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.client_list.customContextMenuRequested.connect(self.context_menu)
        self.server_list.customContextMenuRequested.connect(self.context_menu)

        split_lists = QSplitter(Qt.Horizontal)
        split_lists.addWidget(self.client_list)
        split_lists.addWidget(self.server_list)

        self.inspect_mode = "tree"
        self.inspect_mode_btn = QPushButton()
        self.inspect_mode_btn.clicked.connect(self.toggle_inspect_mode)

        self.inspector = QTreeWidget()
        self.inspector.setHeaderLabels(["Field", "Value"])

        self.details = QTextEdit()
        self.details.setReadOnly(True)
        self.details.hide()

        self.inspect_container = QWidget()
        inspect_layout = QVBoxLayout()
        inspect_layout.setContentsMargins(0, 0, 0, 0)
        inspect_layout.addWidget(self.inspect_mode_btn)
        inspect_layout.addWidget(self.inspector)
        inspect_layout.addWidget(self.details)
        self.inspect_container.setLayout(inspect_layout)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        split_bottom = QSplitter(Qt.Vertical)
        split_bottom.addWidget(self.inspect_container)
        split_bottom.addWidget(self.console)

        main_split = QSplitter(Qt.Vertical)
        main_split.addWidget(top_widget)
        main_split.addWidget(split_lists)
        main_split.addWidget(split_bottom)

        self.setCentralWidget(main_split)

        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(500)

        self.spam_timer = QTimer()
        self.spam_timer.timeout.connect(self.reset_spam_window)
        self.spam_timer.start(self._per_id_hits_window_ms)

        self.apply_lang()
        self._seed_inspector()

    def apply_lang(self):
        self.setWindowTitle(tr(self.lang, "main_title"))
        self.filter_box.setPlaceholderText(tr(self.lang, "filter_ph"))
        self.options_btn.setText(tr(self.lang, "options"))
        self.inspect_mode_btn.setText(tr(self.lang, "mode_tree"))
        self.details.setPlaceholderText(tr(self.lang, "decoded_hint"))
        self.update_stats()

    def _seed_inspector(self):
        self.inspector.clear()
        QTreeWidgetItem(self.inspector, ["NetGarden", tr(self.lang, "tree_hint_left")])
        self.inspector.expandAll()

    def add_packet(self, packet):
        self.packet_signal.emit(packet)

    def add_log(self, message):
        self.log_signal.emit(message)

    def _add_log_safe(self, message):
        self.console.append(message)

    def _json_safe(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, (bytes, bytearray)):
            return obj.hex()
        return str(obj)

    def toggle_inspect_mode(self):
        if self.inspect_mode == "tree":
            self.inspect_mode = "text"
            self.inspect_mode_btn.setText(tr(self.lang, "mode_decode"))
            self.inspector.hide()
            self.details.show()
        else:
            self.inspect_mode = "tree"
            self.inspect_mode_btn.setText(tr(self.lang, "mode_tree"))
            self.details.hide()
            self.inspector.show()

        if self.current_selected_packet is not None:
            self.render_inspection(self.current_selected_packet)

    def _add_packet_safe(self, packet):
        packet_id = getattr(packet, "id", "?")

        if self.auto_hide_spam:
            self._per_id_hits[packet_id] = self._per_id_hits.get(packet_id, 0) + 1
            if self._per_id_hits[packet_id] >= self.spam_threshold_per_sec:
                if packet_id not in self.hidden_ids:
                    self.hidden_ids.add(packet_id)
                    self.console.append(
                        f"[NetGarden] Auto-spam: hiding '{packet_id}' (>= {self.spam_threshold_per_sec}/s)"
                    )

        if packet_id in self.hidden_ids:
            self.hidden_packets.append(packet)
            return

        if self.filter_text and self.filter_text.lower() not in packet_id.lower():
            return

        display_id = packet_id
        if self.string_mode:
            display_id = self.resolve_string(packet_id)

        timestamp = getattr(packet, "timestamp", "")
        direction = getattr(packet, "direction", "")

        text = f"[{timestamp}] {display_id}"

        if direction == "client":
            self.packet_counter_client += 1
            self.client_list.addItem(text)
            item = self.client_list.item(self.client_list.count() - 1)
            self.client_list.scrollToBottom()
        else:
            self.packet_counter_server += 1
            self.server_list.addItem(text)
            item = self.server_list.item(self.server_list.count() - 1)
            self.server_list.scrollToBottom()

        item.setData(Qt.UserRole, packet)
        self.apply_color(item, packet_id)
        self.register_packet_item(packet_id, item)

    def render_inspection(self, packet):
        if self.inspect_mode == "tree":
            self._render_tree(packet)
        else:
            self._render_text(packet)

    def _render_tree(self, packet):
        self.inspector.clear()
        pid = getattr(packet, "id", "")
        direction = getattr(packet, "direction", "")
        timestamp = getattr(packet, "timestamp", "")

        root = QTreeWidgetItem(self.inspector, ["ID", str(pid)])
        QTreeWidgetItem(self.inspector, ["Direction", str(direction)])
        QTreeWidgetItem(self.inspector, ["Time", str(timestamp)])

        parsed = getattr(packet, "parsed", None)
        self.add_tree(root, parsed)
        self.inspector.expandAll()

    def _render_text(self, packet):
        self.details.clear()
        parsed = getattr(packet, "parsed", None)
        if parsed is None:
            self.details.setPlainText(tr(self.lang, "no_bson"))
            return
        try:
            pretty = json.dumps(parsed, indent=2, ensure_ascii=False, default=self._json_safe)
            self.details.setPlainText(pretty)
        except Exception as e:
            self.details.setPlainText(f"Falha ao formatar: {e}\n\n{str(parsed)}")

    def inspect(self, item):
        packet = item.data(Qt.UserRole)
        self.current_selected_packet = packet
        self.render_inspection(packet)

    def add_tree(self, parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    node = QTreeWidgetItem(parent, [str(key), ""])
                    self.add_tree(node, value)
                else:
                    QTreeWidgetItem(parent, [str(key), str(value)])
        elif isinstance(data, list):
            for i, v in enumerate(data):
                node = QTreeWidgetItem(parent, [f"[{i}]", ""])
                self.add_tree(node, v)
        elif data is None:
            QTreeWidgetItem(parent, ["value", "None"])
        else:
            QTreeWidgetItem(parent, ["value", str(data)])

    def set_filter(self, text):
        self.filter_text = text

    def resolve_string(self, packet_id):
        if packet_id in NETSTRINGS:
            return f"{NETSTRINGS[packet_id]} ({packet_id})"
        return packet_id

    def show_options_menu(self):
        menu = QMenu(self)

        act_strings = menu.addAction(tr(self.lang, "opt_string_mode"))
        act_strings.setCheckable(True)
        act_strings.setChecked(self.string_mode)
        act_strings.triggered.connect(lambda _: self.set_string_mode(not self.string_mode))

        act_auto_spam = menu.addAction(tr(self.lang, "opt_auto_spam"))
        act_auto_spam.setCheckable(True)
        act_auto_spam.setChecked(self.auto_hide_spam)
        act_auto_spam.triggered.connect(lambda _: self.set_auto_spam(not self.auto_hide_spam))

        menu.addSeparator()

        act_restore = menu.addAction(tr(self.lang, "opt_restore_spam"))
        act_restore.triggered.connect(self.clear_spams)

        act_saved = menu.addAction(tr(self.lang, "opt_saved"))
        act_saved.triggered.connect(self.open_saved_packets)

        menu.exec(self.options_btn.mapToGlobal(self.options_btn.rect().bottomLeft()))

    def set_string_mode(self, enabled):
        self.string_mode = enabled
        self.console.append(tr(self.lang, "log_string_on" if enabled else "log_string_off"))

    def set_auto_spam(self, enabled):
        self.auto_hide_spam = enabled
        self.console.append(tr(self.lang, "log_spam_on" if enabled else "log_spam_off"))

    def context_menu(self, pos):
        widget = self.sender()
        item = widget.itemAt(pos)
        if not item:
            return

        packet = item.data(Qt.UserRole)
        packet_id = getattr(packet, "id", "")

        menu = QMenu()

        color_menu = menu.addMenu(tr(self.lang, "ctx_color"))
        colors = {
            "Red": QColor(255, 120, 120),
            "Green": QColor(120, 255, 120),
            "Blue": QColor(120, 120, 255),
            "Yellow": QColor(255, 255, 120),
            "Purple": QColor(200, 120, 255),
            "White": QColor(255, 255, 255),
        }
        for name, color in colors.items():
            act = color_menu.addAction(name)
            act.triggered.connect(lambda _, pid=packet_id, col=color: self.set_packet_color(pid, col))

        menu.addSeparator()

        act_view = menu.addAction(tr(self.lang, "ctx_view_full"))
        act_view.triggered.connect(lambda _, p=packet: self._view_full(p))

        act_save = menu.addAction(tr(self.lang, "ctx_save"))
        act_save.triggered.connect(lambda _, p=packet: self.save_packet(p))

        hb = menu.addAction(tr(self.lang, "ctx_mark_hb"))
        hb.triggered.connect(lambda _, pid=packet_id: self.mark_as_spam(pid))

        menu.exec(widget.mapToGlobal(pos))

    def _view_full(self, packet):
        self.inspect_mode = "text"
        self.inspect_mode_btn.setText(tr(self.lang, "mode_decode"))
        self.inspector.hide()
        self.details.show()
        self.current_selected_packet = packet
        self._render_text(packet)

    def mark_as_spam(self, packet_id):
        self.hidden_ids.add(packet_id)
        self.console.append(f"[NetGarden] Hidden as spam/heartbeat: {packet_id}")

    def clear_spams(self):
        if not self.hidden_ids and not self.hidden_packets:
            self.console.append(tr(self.lang, "log_no_spams"))
            return
        self.console.append(tr(self.lang, "log_restore_hidden"))
        self.hidden_ids.clear()

        cached = self.hidden_packets
        self.hidden_packets = []
        for pkt in cached:
            self._add_packet_safe(pkt)

    def save_packet(self, packet):
        self.saved_packets.append({
            "id": getattr(packet, "id", ""),
            "direction": getattr(packet, "direction", ""),
            "timestamp": getattr(packet, "timestamp", ""),
            "packet": packet
        })
        self.console.append(tr(self.lang, "log_saved", id=getattr(packet, "id", "")))

    def open_saved_packets(self):
        from NetGarden.GUI.SavedPacketsWindow import SavedPacketsWindow

        def get_saved():
            return self.saved_packets

        def jump_to(saved_index):
            if saved_index < 0 or saved_index >= len(self.saved_packets):
                return
            pkt = self.saved_packets[saved_index]["packet"]
            self.jump_to_packet(pkt)

        if self.saved_window is None:
            self.saved_window = SavedPacketsWindow(self.lang, get_saved, jump_to)
        else:
            self.saved_window.lang = self.lang
            self.saved_window.apply_lang()

        self.saved_window.refresh()
        self.saved_window.show()
        self.saved_window.raise_()
        self.saved_window.activateWindow()

    def jump_to_packet(self, packet):
        pid = getattr(packet, "id", "")
        ts = getattr(packet, "timestamp", "")
        direction = getattr(packet, "direction", "")

        target_list = self.client_list if direction == "client" else self.server_list

        for i in range(target_list.count()):
            item = target_list.item(i)
            p = item.data(Qt.UserRole)
            if p is packet:
                target_list.setCurrentItem(item)
                target_list.scrollToItem(item)
                self.inspect(item)
                return

        for i in range(target_list.count()):
            item = target_list.item(i)
            p = item.data(Qt.UserRole)
            if getattr(p, "id", "") == pid and getattr(p, "timestamp", "") == ts:
                target_list.setCurrentItem(item)
                target_list.scrollToItem(item)
                self.inspect(item)
                return

    def set_packet_color(self, packet_id, color):
        self.packet_colors[packet_id] = color
        if packet_id in self.packet_items_by_id:
            for it in self.packet_items_by_id[packet_id]:
                it.setBackground(color)

    def apply_color(self, item, packet_id):
        if packet_id in self.packet_colors:
            item.setBackground(self.packet_colors[packet_id])

    def register_packet_item(self, packet_id, item):
        if packet_id not in self.packet_items_by_id:
            self.packet_items_by_id[packet_id] = []
        self.packet_items_by_id[packet_id].append(item)

    def update_stats(self):
        total = self.packet_counter_client + self.packet_counter_server
        self.stats_label.setText(tr(self.lang, "stats", total=total, client=self.packet_counter_client, server=self.packet_counter_server))

    def reset_spam_window(self):
        self._per_id_hits.clear()