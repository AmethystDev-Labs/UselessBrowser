import json
import os
import platform
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional
from urllib.request import urlopen


KNOWN_GOOD_VERSIONS_URL = (
    'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'
)

BROWSER_ARGS = [
    '--disable-dev-shm-usage',
]


@dataclass
class BrowserEntry:
    id: str
    name: str
    version: str
    path: Path
    source: str


def get_browsers_dir() -> Path:
    base_dir = Path(__file__).resolve().parent.parent
    browsers_dir = base_dir / 'browsers'
    browsers_dir.mkdir(parents=True, exist_ok=True)
    return browsers_dir


def fetch_known_good_versions(url: str = KNOWN_GOOD_VERSIONS_URL) -> dict:
    with urlopen(url, timeout=20) as response:
        payload = response.read()
    return json.loads(payload.decode('utf-8'))


def parse_chrome_downloads(data: dict) -> dict[str, list[dict]]:
    versions = {}
    for entry in data.get('versions', []):
        version = entry.get('version')
        downloads = entry.get('downloads', {}).get('chrome', [])
        if version and downloads:
            versions[version] = downloads
    return versions


def install_chrome_download(download_url: str, version: str, target_dir: Optional[Path] = None) -> Path:
    browsers_dir = target_dir or get_browsers_dir()
    version_dir = browsers_dir / version
    if version_dir.exists() and any(version_dir.iterdir()):
        raise FileExistsError(f'Browser {version} already installed.')

    version_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix='chrome_download_'))
    archive_path = temp_dir / 'chrome.zip'
    try:
        with urlopen(download_url, timeout=60) as response, open(archive_path, 'wb') as handle:
            shutil.copyfileobj(response, handle)

        with zipfile.ZipFile(archive_path, 'r') as archive:
            archive.extractall(version_dir)
    except Exception:
        shutil.rmtree(version_dir, ignore_errors=True)
        raise
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
    return version_dir


def _build_entry(path: Path, name: str, version: str, source: str) -> BrowserEntry:
    resolved = path.resolve()
    return BrowserEntry(
        id=str(resolved),
        name=name,
        version=version,
        path=resolved,
        source=source,
    )


def _extract_version_from_path(path: Path, browsers_dir: Path) -> str:
    try:
        rel = path.resolve().relative_to(browsers_dir.resolve())
        if rel.parts:
            return rel.parts[0]
    except Exception:
        pass
    return 'unknown'


def scan_local_browsers() -> list[BrowserEntry]:
    browsers_dir = get_browsers_dir()
    entries: list[BrowserEntry] = []

    exe_names = ['chrome.exe'] if platform.system() == 'Windows' else ['chrome', 'Chromium']
    for exe_name in exe_names:
        for path in browsers_dir.rglob(exe_name):
            if not path.is_file():
                continue
            version = _extract_version_from_path(path, browsers_dir)
            entries.append(_build_entry(path, 'Chrome', version, 'local'))
    return entries


def scan_system_browsers() -> list[BrowserEntry]:
    system = platform.system()
    candidates: list[tuple[str, str]] = []

    if system == 'Windows':
        candidates = [
            ('Chrome', os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe')),
            ('Chrome', os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe')),
            ('Chrome', os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe')),
            ('Chromium', os.path.expandvars(r'%ProgramFiles%\Chromium\Application\chrome.exe')),
            ('Chromium', os.path.expandvars(r'%LocalAppData%\Chromium\Application\chrome.exe')),
            ('Edge', os.path.expandvars(r'%ProgramFiles%\Microsoft\Edge\Application\msedge.exe')),
            ('Edge', os.path.expandvars(r'%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe')),
            ('Brave', os.path.expandvars(r'%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe')),
            ('Brave', os.path.expandvars(r'%ProgramFiles(x86)%\BraveSoftware\Brave-Browser\Application\brave.exe')),
        ]
    elif system == 'Darwin':
        candidates = [
            ('Chrome', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
            ('Chromium', '/Applications/Chromium.app/Contents/MacOS/Chromium'),
            ('Edge', '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'),
            ('Brave', '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'),
        ]
    else:
        candidates = [
            ('Chrome', '/usr/bin/google-chrome'),
            ('Chrome', '/usr/bin/google-chrome-stable'),
            ('Chromium', '/usr/bin/chromium'),
            ('Chromium', '/usr/bin/chromium-browser'),
            ('Edge', '/usr/bin/microsoft-edge'),
            ('Brave', '/usr/bin/brave-browser'),
        ]

    entries: list[BrowserEntry] = []
    for name, path in candidates:
        path_obj = Path(path)
        if path_obj.exists():
            entries.append(_build_entry(path_obj, name, 'system', 'system'))
    return entries


def dedupe_entries(entries: Iterable[BrowserEntry]) -> list[BrowserEntry]:
    seen = set()
    result = []
    for entry in entries:
        key = str(entry.path.resolve())
        if key in seen:
            continue
        seen.add(key)
        result.append(entry)
    return result


def load_browser_library() -> list[BrowserEntry]:
    entries = scan_local_browsers() + scan_system_browsers()
    return dedupe_entries(entries)


def find_chrome_path() -> Optional[str]:
    """Finds the best available Chrome/Chromium executable path."""
    entries = scan_system_browsers()
    if not entries:
        entries = scan_local_browsers()
    
    # Prefer Chrome over others, or just pick the first one
    for entry in entries:
        if 'Chrome' in entry.name:
            return str(entry.path)
    
    if entries:
        return str(entries[0].path)
        
    return None


def remove_local_browser(entry: BrowserEntry, browsers_dir: Optional[Path] = None) -> Path:
    if entry.source != 'local':
        raise ValueError('Only local browsers can be removed.')
    browsers_dir = browsers_dir or get_browsers_dir()
    resolved_entry = entry.path.resolve()
    try:
        rel = resolved_entry.relative_to(browsers_dir.resolve())
    except Exception as exc:
        raise ValueError('Browser is not under local browsers dir.') from exc
    if not rel.parts:
        raise ValueError('Invalid local browser path.')
    target_dir = browsers_dir / rel.parts[0]
    if target_dir.exists():
        shutil.rmtree(target_dir)
    return target_dir
