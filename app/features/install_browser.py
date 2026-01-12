import os
import sys
from typing import Optional

from qfluentwidgets import InfoBar, InfoBarPosition

from app.browser_library import KNOWN_GOOD_VERSIONS_URL, parse_chrome_downloads
from app.workers import BrowserInstallWorker, BrowserVersionsWorker


class InstallBrowserMixin:
    def _detect_platform_key(self) -> Optional[str]:
        system = os.name
        if system == 'nt':
            return 'win64'
        if system == 'posix' and sys.platform == 'darwin':
            return 'mac-arm64'
        if system == 'posix':
            return 'linux64'
        return None

    def _load_browser_versions(self) -> None:
        if self._browser_versions_worker and self._browser_versions_worker.isRunning():
            return
        self._set_install_busy(True, context=None)
        self._log('Loading versions...')
        self._browser_versions_worker = BrowserVersionsWorker(KNOWN_GOOD_VERSIONS_URL)
        self._browser_versions_worker.finished.connect(self._on_versions_loaded)
        self._browser_versions_worker.start()

    def _on_versions_loaded(self, success: bool, data: Optional[dict], message: str) -> None:
        self._set_install_busy(False, context=None)
        if not success or not data:
            self._log(f'Failed to load versions: {message}')
            InfoBar.error(
                title=self._t('install_browser_failed_title'),
                content=message or self._t('install_browser_load_failed'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return
        self._browser_versions = parse_chrome_downloads(data)
        versions = sorted(self._browser_versions.keys(), reverse=True)
        versions = versions[: self._max_browser_versions]
        for combo, button, _ in self._install_widget_sets():
            combo.blockSignals(True)
            combo.clear()
            for version in versions:
                combo.addItem(version, version)
            combo.blockSignals(False)
            platform_key = self._detect_platform_key()
            selected_index = 0
            if platform_key:
                for idx, version in enumerate(versions):
                    downloads = self._browser_versions.get(version, [])
                    if any(item.get('platform') == platform_key for item in downloads):
                        selected_index = idx
                        break
            if versions:
                combo.setCurrentIndex(selected_index)
            button.setEnabled(bool(versions) and bool(platform_key))
        self._log(f'Loaded {len(versions)} versions.')

    def _on_install_version_changed(self, index: int) -> None:
        combo, button, _ = self._install_widgets_for_sender(self.sender())
        version = combo.itemData(index)
        if not version:
            version = combo.currentText().strip()
        version = str(version)
        downloads = self._browser_versions.get(version, [])
        self._log(f'Version changed: {version} ({len(downloads)} downloads)')
        platform_key = self._detect_platform_key()
        if platform_key:
            self._log(f'Auto platform: {platform_key}')
        button.setEnabled(bool(version) and bool(platform_key))

    def _start_install_browser(self) -> None:
        combo, button, _ = self._install_widgets_for_sender(self.sender())
        if self._browser_install_worker and self._browser_install_worker.isRunning():
            self._log('Install already running')
            return
        version = combo.currentData()
        if not version:
            version = combo.currentText().strip()
        platform_name = self._detect_platform_key()
        if not version or not platform_name:
            self._log(f'Install blocked: version={version}, platform={platform_name}')
            InfoBar.warning(
                title=self._t('install_browser_failed_title'),
                content=self._t('install_browser_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return
        downloads = self._browser_versions.get(version, [])
        download_url = None
        for item in downloads:
            if item.get('platform') == platform_name:
                download_url = item.get('url')
                break
        if not download_url:
            self._log(f'No download url for version={version}, platform={platform_name}')
            InfoBar.error(
                title=self._t('install_browser_failed_title'),
                content=self._t('install_browser_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return
        self._install_context = self._install_context_for_widgets(combo)
        self._set_install_busy(True, context=self._install_context)
        self._log(f'Start install version={version} platform={platform_name}')
        self._browser_install_worker = BrowserInstallWorker(download_url, version)
        self._browser_install_worker.finished.connect(self._on_install_finished)
        self._browser_install_worker.start()

    def _on_install_finished(self, success: bool, message: str) -> None:
        self._set_install_busy(False, context=getattr(self, '_install_context', 'main'))
        if success:
            self._log('Install complete')
            InfoBar.success(
                title=self._t('install_browser_success_title'),
                content=self._t('install_browser_success_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            self.refresh_browser_library()
        else:
            self._log(f'Install failed: {message}')
            InfoBar.error(
                title=self._t('install_browser_failed_title'),
                content=message or self._t('install_browser_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )

    def _set_install_busy(self, busy: bool, context: Optional[str] = 'main') -> None:
        if context is None:
            for _, _, progress in self._install_widget_sets():
                progress.setVisible(busy)
            for combo, button, _ in self._install_widget_sets():
                combo.setEnabled(not busy)
                button.setEnabled(not busy)
            return
        combo, button, progress = self._install_widgets_for_context(context)
        progress.setVisible(busy)
        combo.setEnabled(not busy)
        button.setEnabled(not busy)

    def _install_widget_sets(self) -> list[tuple]:
        sets = [
            (self.install_version_combo, self.install_browser_btn, self.install_progress),
        ]
        if hasattr(self, 'onboarding_install_version_combo'):
            sets.append(
                (
                    self.onboarding_install_version_combo,
                    self.onboarding_install_btn,
                    self.onboarding_install_progress,
                )
            )
        return sets

    def _install_widgets_for_sender(self, sender) -> tuple:
        if sender is getattr(self, 'onboarding_install_version_combo', None) or sender is getattr(
            self, 'onboarding_install_btn', None
        ):
            return (
                self.onboarding_install_version_combo,
                self.onboarding_install_btn,
                self.onboarding_install_progress,
            )
        return (self.install_version_combo, self.install_browser_btn, self.install_progress)

    def _install_context_for_widgets(self, combo) -> str:
        if combo is getattr(self, 'onboarding_install_version_combo', None):
            return 'onboarding'
        return 'main'

    def _install_widgets_for_context(self, context: str) -> tuple:
        if context == 'onboarding':
            return (
                self.onboarding_install_version_combo,
                self.onboarding_install_btn,
                self.onboarding_install_progress,
            )
        return (self.install_version_combo, self.install_browser_btn, self.install_progress)
