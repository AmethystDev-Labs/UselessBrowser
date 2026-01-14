import traceback
from typing import Optional, Any

from PyQt6 import QtCore

from app.browser_library import fetch_known_good_versions, install_chrome_download
from urllib.error import URLError
import json
from spoofers.profile import ProfileConfig, BaseConfig


class BrowserLaunchWorker(QtCore.QThread):
    finished = QtCore.pyqtSignal(bool, str)

    def __init__(self, profile_id: str, profile: ProfileConfig, url: str, browser_path: Optional[str] = None):
        super().__init__()
        self.profile_id = profile_id
        self.profile = profile
        self.url = url
        self.browser_path = browser_path
        self.page: Any = None

    def run(self) -> None:
        try:
            from app.adapters.registry import get_adapter
            adapter = get_adapter(self.profile.base_config.adapter_id)

            base = BaseConfig.from_dict(self.profile.base_config.to_dict(), self.profile_id)
            if self.url:
                base.target_url = self.url
            if self.browser_path:
                base.browser_path = self.browser_path

            result = adapter.launch(base, self.profile.extra_config or {})
            self.page = result.page
            self.finished.emit(True, '')
        except Exception:
            self.finished.emit(False, traceback.format_exc())


class BrowserVersionsWorker(QtCore.QThread):
    finished = QtCore.pyqtSignal(bool, object, str)

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self) -> None:
        try:
            data = fetch_known_good_versions(self.url)
            self.finished.emit(True, data, '')
        except (URLError, json.JSONDecodeError, OSError) as exc:
            self.finished.emit(False, None, str(exc))


class BrowserInstallWorker(QtCore.QThread):
    finished = QtCore.pyqtSignal(bool, str)

    def __init__(self, download_url: str, version: str):
        super().__init__()
        self.download_url = download_url
        self.version = version

    def run(self) -> None:
        try:
            install_chrome_download(self.download_url, self.version)
            self.finished.emit(True, '')
        except Exception as exc:
            self.finished.emit(False, str(exc))
