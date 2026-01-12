import traceback
from typing import Optional

from DrissionPage import ChromiumPage
from PyQt6 import QtCore

from app.profile_utils import build_chromium_options
from app.browser_library import fetch_known_good_versions, install_chrome_download
from urllib.error import URLError
import json
from spoofers.cdp_spoofer import apply_pre_navigation_spoofing
from spoofers.profile import SpoofProfile


class BrowserLaunchWorker(QtCore.QThread):
    finished = QtCore.pyqtSignal(bool, str)

    def __init__(self, profile_id: str, profile: SpoofProfile, url: str, browser_path: Optional[str] = None):
        super().__init__()
        self.profile_id = profile_id
        self.profile = profile
        self.url = url
        self.browser_path = browser_path
        self.page: Optional[ChromiumPage] = None

    def run(self) -> None:
        try:
            co = build_chromium_options(self.profile_id, self.browser_path)
            page = ChromiumPage(co)
            apply_pre_navigation_spoofing(page, self.profile)
            page.get(self.url)
            self.page = page
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
