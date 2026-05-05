import json
import os
from datetime import datetime

HISTORY_FILE = "password_history.json"

def load_history():
    """Загружает историю паролей из JSON-файла."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю паролей в JSON-файл."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(password, length, use_letters, use_digits, use_special):
    """Добавляет новый пароль в историю."""
    history = load_history()
    entry = {
        "password": password,
        "length": length,
        "use_letters": use_letters,
        "use_digits": use_digits,
        "use_special": use_special,
        "timestamp": datetime.now().isoformat()
    }
    history.append(entry)
    save_history(history)
