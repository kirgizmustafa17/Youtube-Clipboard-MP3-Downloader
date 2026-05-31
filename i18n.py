import os
import sys
import json
import locale
import ctypes

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# AppData klasörü (Zaten main.py ve updater.py tarafından oluşturuluyor)
appdata_dir = os.path.join(os.getenv('APPDATA'), 'YTAudioCatcher')
config_path = os.path.join(appdata_dir, 'config.json')

def load_config():
    if not os.path.exists(appdata_dir):
        os.makedirs(appdata_dir, exist_ok=True)
        
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
            
    # Default config
    default_config = {"language": "auto"}
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
    except Exception:
        pass
    return default_config

def get_system_language():
    try:
        windll = ctypes.windll.kernel32
        lang_id = windll.GetUserDefaultUILanguage()
        # Türkçe'nin lang_id'si 1055 (0x041F)
        if lang_id == 1055:
            return "tr"
    except Exception:
        pass
    
    try:
        loc = locale.getdefaultlocale()[0]
        if loc and loc.lower().startswith('tr'):
            return "tr"
    except Exception:
        pass
        
    return "en"

def init_i18n():
    config = load_config()
    lang = config.get("language", "auto")
    
    if lang == "auto":
        lang = get_system_language()
        
    if lang not in ["tr", "en"]:
        lang = "en"
        
    locale_file = os.path.join(get_base_dir(), 'locales', f'{lang}.json')
    if not os.path.exists(locale_file):
        # Fallback to english
        locale_file = os.path.join(get_base_dir(), 'locales', 'en.json')
        
    try:
        with open(locale_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

# Load translations on module import
translations = init_i18n()

def tr(key, **kwargs):
    text = translations.get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text
