import json
import os
import datetime

CONFIG_FILE = "config.json"
HISTORY_FILE = "history.json"

class DataManager:
    def __init__(self):
        self.settings = self._load_settings()
        self.history = self._load_history()

    def _load_settings(self):
        default = {"default_quality": "1080p", "dark_mode": False}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return {**default, **json.load(f)}
            except: pass
        return default

    def save_settings(self, settings_dict):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(settings_dict, f)
            self.settings = settings_dict
        except Exception as e:
            print(f"Błąd zapisu ustawień: {e}")

    def _load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: pass
        return []

    def add_history_entry(self, title, url, path):
        entry = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "title": title,
            "url": url,
            "path": path
        }
        self.history.insert(0, entry)
        self.rewrite_history_file()

    def rewrite_history_file(self):
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Błąd zapisu historii: {e}")