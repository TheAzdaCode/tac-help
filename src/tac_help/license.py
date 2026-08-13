# license.py — управление лицензиями (версия 0.2.0)

import os
import json
import requests
from pathlib import Path
from datetime import datetime

LICENSE_FILE = Path.home() / ".tac_license"
JSONBIN_URL = "https://api.jsonbin.io/v3/b/6a7d89d8da38895dfedec667"
JSONBIN_ACCESS_KEY = "$2a$10$ZftfS.Kws7QbwQ0BjDlB4.CB5UiT3OJ5zlBUzrsPRc952pzK4iyEe"

TIER_LEVELS = {
    "free": 0,
    "pro": 1,
    "premium": 2,
    "vip": 3,
    "master": 99
}

PLAYEROK_URL = "https://playerok.com/profile/TLookShop/products"

def load_license():
    if LICENSE_FILE.exists():
        with open(LICENSE_FILE, "r") as f:
            data = json.load(f)
            return data.get("key")
    return None

def save_license(key):
    with open(LICENSE_FILE, "w") as f:
        json.dump({"key": key}, f)

def fetch_keys():
    headers = {"X-Access-Key": JSONBIN_ACCESS_KEY}
    try:
        response = requests.get(JSONBIN_URL, headers=headers)
        if response.status_code == 200:
            return response.json().get("record", {}).get("keys", {})
    except:
        pass
    return {}

def validate_key(key):
    keys = fetch_keys()
    if key not in keys:
        return None, "Неверный ключ"
    key_info = keys[key]
    expires = key_info.get("expires")
    if expires != "never":
        try:
            end = datetime.strptime(expires, "%Y-%m-%d").date()
            now = datetime.now().date()
            if end < now:
                return None, "Срок действия истёк"
            delta = (end - now).days
            if delta <= 7:
                print(f"⚠️ Ваш ключ истекает через {delta} дней. Продлите подписку!")
        except:
            return None, "Ошибка формата даты"
    return key_info.get("tier"), None

def get_tier():
    key = load_license()
    if not key:
        return "free"
    tier, error = validate_key(key)
    if error:
        print(f"❌ {error}")
        return "free"
    return tier

def has_access(required_tier):
    current = get_tier()
    current_level = TIER_LEVELS.get(current, 0)
    required_level = TIER_LEVELS.get(required_tier, 0)
    return current_level >= required_level

def activate(key):
    tier, error = validate_key(key)
    if error:
        return False, error
    save_license(key)
    return True, f"Активирован доступ: {tier}"

def set_license_key(key):
    return activate(key)

def ask_for_license():
    print("🔑 Введите лицензионный ключ TAC (или оставьте пустым для бесплатной версии):")
    key = input("> ").strip()
    if not key:
        return "free"
    success, msg = activate(key)
    if success:
        print(f"✅ {msg}")
    else:
        print(f"❌ {msg}")
    return get_tier()