from typing import Optional, Any

from PyQt6 import QtWidgets

from qfluentwidgets import FluentWindow
from qfluentwidgets.common.translator import FluentTranslator
from qfluentwidgets.common.theme_listener import SystemThemeListener

from app.app_config import DEFAULT_APP_SETTINGS, resolve_language_code
from app.ui_strings import UI_STRINGS
from app.ui_builders import (
    build_home_page,
    build_launch_page,
    build_profiles_page,
    build_settings_page,
    build_onboarding_page,
    build_browser_library_page,
    build_install_browser_page,
    build_navigation,
)
from app.workers import BrowserInstallWorker, BrowserLaunchWorker, BrowserVersionsWorker
from app.features.base import AppLogMixin
from app.features.home import HomeMixin
from app.features.settings import SettingsMixin
from app.features.profiles import ProfilesMixin
from app.features.launch import LaunchMixin
from app.features.browser_library import BrowserLibraryMixin
from app.features.install_browser import InstallBrowserMixin
from app.features.onboarding import OnboardingMixin
from spoofers.profile import ProfileConfig


class MainWindow(
    FluentWindow,
    AppLogMixin,
    HomeMixin,
    SettingsMixin,
    ProfilesMixin,
    LaunchMixin,
    BrowserLibraryMixin,
    InstallBrowserMixin,
    OnboardingMixin,
):
    def __init__(self, settings: Optional[dict] = None) -> None:
        super().__init__()
        self._app_settings = settings or DEFAULT_APP_SETTINGS.copy()
        self._language_mode = self._app_settings.get('language', 'system')
        self._theme_mode = self._app_settings.get('theme', 'auto')
        self._language_code = resolve_language_code(self._language_mode)
        self._strings = UI_STRINGS[self._language_code]
        self._fluent_translator: Optional[FluentTranslator] = None
        self._theme_listener = SystemThemeListener(self)
        self._theme_listener.systemThemeChanged.connect(self._on_system_theme_changed)
        self._palette_labels: list[QtWidgets.QLabel] = []
        self._palette_group_boxes: list[QtWidgets.QGroupBox] = []

        self._apply_fluent_translator()
        self._apply_theme(self._theme_mode, save=False)

        self.setWindowTitle(self._t('window_title'))
        self.resize(1000, 650)
        self.setMinimumSize(520, 360)
        self._pages: list[Any] = []
        self._current_profile_id: Optional[str] = None
        self._current_profile: Optional[ProfileConfig] = None
        self._launch_worker: Optional[BrowserLaunchWorker] = None
        self._browser_versions_worker: Optional[BrowserVersionsWorker] = None
        self._browser_install_worker: Optional[BrowserInstallWorker] = None
        self._updating_protection = False
        self._updating_launch_combo = False
        self._updating_browser_combo = False
        self._updating_profile_controls = False
        self._user_name = self._resolve_user_name()
        self._home_edit_mode = False
        self._browser_entries = []
        self._browser_versions = {}
        self._max_browser_versions = 200
        self._browser_combo_ids: list[str] = []
        self._onboarding_checked = False

        self._build_ui()
        self.hBoxLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.navigationInterface.setStyleSheet('border: none;')
        self.stackedWidget.setStyleSheet('border: none;')
        self.install_version_combo.currentIndexChanged.connect(self._on_install_version_changed)
        self.refresh_profiles()
        self.refresh_browser_library()
        self._load_browser_versions()
        self._apply_language()
        self._sync_settings_controls()
        self._apply_palette_overrides()
        self._maybe_start_onboarding()

    def _build_ui(self) -> None:
        build_home_page(self)
        build_launch_page(self)
        build_profiles_page(self)
        build_browser_library_page(self)
        build_install_browser_page(self)
        build_settings_page(self)
        build_onboarding_page(self)
        build_navigation(self)

    def _t(self, key: str) -> str:
        return self._strings.get(key, key)

    def closeEvent(self, event) -> None:  # noqa: N802
        if self._theme_listener.isRunning():
            self._theme_listener.requestInterruption()
            self._theme_listener.wait(1500)
        for worker in (self._browser_versions_worker, self._browser_install_worker, self._launch_worker):
            if worker and worker.isRunning():
                worker.wait(1500)
        for page in self._pages:
            try:
                page.quit()
            except Exception:
                pass
        event.accept()
