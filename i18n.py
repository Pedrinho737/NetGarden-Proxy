import json
import os

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")

LANG_PT = "pt-BR"
LANG_EN = "en"

STRINGS = {
    LANG_PT: {
        "app_launcher_title": "NetGarden 🌱 | Launcher",
        "start_proxy": "Iniciar Proxy",
        "client_ip": "IP do Client:",
        "client_port": "Porta do Client:",
        "server_ip": "IP do Server:",
        "server_port": "Porta do Server:",
        "local_btn": "Local (127.0.0.1)",
        "recents": "Conexões recentes:",
        "clear_recents": "Limpar recentes",
        "invalid_ports": "As portas precisam ser números.",
        "language": "Idioma:",
        "ptbr": "Português (BR)",
        "en": "English",

        "main_title": "NetGarden 🌱",
        "filter_ph": "Filtrar por ID...",
        "options": "Opções",
        "stats": "Pacotes: {total} | Client: {client} | Server: {server}",

        "mode_tree": "Modo: Árvore",
        "mode_decode": "Modo: Decodificar",
        "tree_hint_left": "Clique em um pacote",
        "decoded_hint": "Decodificado (JSON) aparecerá aqui...",
        "no_packet": "Nenhum pacote.",
        "no_bson": "Sem BSON parseado (raw/unknown).",

        "ctx_color": "Por cor",
        "ctx_view_full": "Ver por extenso",
        "ctx_save": "Salvar pacote",
        "ctx_mark_hb": "Marcar como Heartbeat (ocultar)",

        "opt_string_mode": "Ver em string (BETA)",
        "opt_auto_spam": "Auto-ocultar spam",
        "opt_restore_spam": "Restaurar spam",
        "opt_saved": "Pacotes salvos",

        "log_string_on": "[NetGarden] String mode: ON",
        "log_string_off": "[NetGarden] String mode: OFF",
        "log_spam_on": "[NetGarden] Auto-spam: ON",
        "log_spam_off": "[NetGarden] Auto-spam: OFF",
        "log_restore_hidden": "[NetGarden] Restoring hidden packets...",
        "log_no_spams": "[NetGarden] No spams to restore",
        "log_saved": "[NetGarden] Pacote salvo: {id}",

        "saved_title": "NetGarden 🌱 | Pacotes salvos",
        "saved_hint": "Clique em um pacote para pular até ele:",
    },

    LANG_EN: {
        "app_launcher_title": "NetGarden 🌱 | Launcher",
        "start_proxy": "Start Proxy",
        "client_ip": "Client IP:",
        "client_port": "Client Port:",
        "server_ip": "Server IP:",
        "server_port": "Server Port:",
        "local_btn": "Local (127.0.0.1)",
        "recents": "Recent connections:",
        "clear_recents": "Clear recents",
        "invalid_ports": "Ports must be numbers.",
        "language": "Language:",
        "ptbr": "Português (BR)",
        "en": "English",

        "main_title": "NetGarden 🌱",
        "filter_ph": "Filter by ID...",
        "options": "Options",
        "stats": "Packets: {total} | Client: {client} | Server: {server}",

        "mode_tree": "Mode: Tree",
        "mode_decode": "Mode: Decode",
        "tree_hint_left": "Click a packet",
        "decoded_hint": "Decoded (JSON) will appear here...",
        "no_packet": "No packet.",
        "no_bson": "No parsed BSON (raw/unknown).",

        "ctx_color": "By color",
        "ctx_view_full": "View decoded",
        "ctx_save": "Save packet",
        "ctx_mark_hb": "Mark as Heartbeat (hide)",

        "opt_string_mode": "String mode (BETA)",
        "opt_auto_spam": "Auto-hide spam",
        "opt_restore_spam": "Restore spam",
        "opt_saved": "Saved packets",

        "log_string_on": "[NetGarden] String mode: ON",
        "log_string_off": "[NetGarden] String mode: OFF",
        "log_spam_on": "[NetGarden] Auto-spam: ON",
        "log_spam_off": "[NetGarden] Auto-spam: OFF",
        "log_restore_hidden": "[NetGarden] Restoring hidden packets...",
        "log_no_spams": "[NetGarden] No spams to restore",
        "log_saved": "[NetGarden] Saved packet: {id}",

        "saved_title": "NetGarden 🌱 | Saved packets",
        "saved_hint": "Click a packet to jump to it:",
    }
}


def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        return {"lang": LANG_PT}
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {"lang": LANG_PT}
        return {"lang": data.get("lang", LANG_PT)}
    except:
        return {"lang": LANG_PT}


def save_settings(settings):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except:
        pass


def tr(lang, key, **kwargs):
    pack = STRINGS.get(lang, STRINGS[LANG_PT])
    text = pack.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text