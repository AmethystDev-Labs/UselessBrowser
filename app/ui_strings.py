import json
from pathlib import Path


def _load_strings(locale: str) -> dict:
    base_dir = Path(__file__).resolve().parent.parent
    path = base_dir / 'i18n' / f'{locale}.json'
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


UI_STRINGS = {
    'en-US': _load_strings('en-US'),
    'zh-CN': _load_strings('zh-CN'),
}
