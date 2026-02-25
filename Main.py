import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from NetGarden.GUI.i18n import load_settings
from NetGarden.GUI.ConfigWindow import ConfigWindow
from NetGarden.GUI.MainWindow import MainWindow
from NetGarden.CORE.Proxy import Proxy


def main():
    app = QApplication(sys.argv)

    settings = load_settings()
    lang = settings.get("lang", "pt-BR")

    main_window = MainWindow(lang)
    proxy_holder = {"proxy": None}
    config_window = None

    def reopen_launcher():
        main_window.hide()
        config_window.show()

    def on_proxy_closed():
        QTimer.singleShot(0, reopen_launcher)

    def on_start(cfg):
        nonlocal main_window
        # se mudar idioma no launcher, aplica aqui
        lang2 = cfg.get("lang", lang)
        main_window.lang = lang2
        main_window.apply_lang()

        main_window.show()
        config_window.hide()

        proxy = Proxy(
            listen_host=cfg["client_ip"],
            listen_port=cfg["client_port"],
            server_host=cfg["server_ip"],
            server_port=cfg["server_port"],
            on_packet=main_window.add_packet,
            on_log=main_window.add_log,
            on_close=on_proxy_closed
        )
        proxy_holder["proxy"] = proxy
        proxy.start()

    config_window = ConfigWindow(on_start=on_start, lang=lang)
    config_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()