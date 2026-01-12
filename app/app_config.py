import json
from pathlib import Path

from PyQt6 import QtCore
from qfluentwidgets.common import Theme

APP_SETTINGS_PATH = Path('config/app.json')
DEFAULT_APP_SETTINGS = {
    'language': 'system',
    'theme': 'auto',
}


def load_app_settings() -> dict:
    if APP_SETTINGS_PATH.exists():
        try:
            data = json.loads(APP_SETTINGS_PATH.read_text(encoding='utf-8'))
            return {**DEFAULT_APP_SETTINGS, **data}
        except Exception:
            return DEFAULT_APP_SETTINGS.copy()
    return DEFAULT_APP_SETTINGS.copy()


def save_app_settings(settings: dict) -> None:
    APP_SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    APP_SETTINGS_PATH.write_text(json.dumps(settings, indent=2), encoding='utf-8')


def resolve_language_code(language: str) -> str:
    if language == 'system':
        system_locale = QtCore.QLocale.system().name().replace('_', '-')
        return 'zh-CN' if system_locale.startswith('zh') else 'en-US'
    if language.startswith('zh'):
        return 'zh-CN'
    return 'en-US'


def resolve_theme_mode(theme: str) -> Theme:
    if theme == 'dark':
        return Theme.DARK
    if theme == 'light':
        return Theme.LIGHT
    return Theme.AUTO
