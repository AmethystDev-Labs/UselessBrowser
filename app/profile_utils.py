import json
from typing import Optional

from DrissionPage import ChromiumOptions

from app.spoofers.profile import get_profiles_dir


def list_profile_entries() -> list[dict]:
    profiles_dir = get_profiles_dir()
    entries = []
    for path in sorted(profiles_dir.glob('*.json')):
        display = path.stem
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            display = data.get('email') or display
        except Exception:
            pass
        entries.append({'id': path.stem, 'display': display, 'path': path})
    return entries


def build_chromium_options(profile_id: str, browser_path: Optional[str] = None) -> ChromiumOptions:
    co = ChromiumOptions()

    profiles_dir = get_profiles_dir()
    user_data_dir = profiles_dir / 'chrome' / profile_id
    user_data_dir.mkdir(parents=True, exist_ok=True)
    co.set_user_data_path(str(user_data_dir))
    co.auto_port()

    co.set_argument('--disable-infobars')
    co.set_argument('--no-first-run')
    co.set_argument('--no-default-browser-check')
    co.set_argument('--disable-dev-shm-usage')

    try:
        from app.browser_library import find_chrome_path, BROWSER_ARGS

        chrome_path = browser_path or find_chrome_path()
        if chrome_path:
            co.set_browser_path(chrome_path)
        for arg in BROWSER_ARGS:
            co.set_argument(arg)
    except Exception:
        if browser_path:
            co.set_browser_path(browser_path)

    return co
