from typing import Optional

from PyQt6 import QtWidgets
from qfluentwidgets import InfoBar, InfoBarPosition

from app.workers import BrowserLaunchWorker
from app.spoofers.profile import load_profile


def resolve_effective_profile_id(
    launch_profile_id: Optional[str],
    current_profile_id: Optional[str],
) -> Optional[str]:
    return launch_profile_id or current_profile_id


class LaunchMixin:
    def _resolve_launch_profile_id(self) -> Optional[str]:
        idx = self.launch_profile_combo.currentIndex()
        if idx <= 0:
            return None
        value = None
        try:
            value = self.launch_profile_combo.itemData(idx)
        except Exception:
            value = None
        if value:
            return value
        try:
            value = self.launch_profile_combo.currentData()
        except Exception:
            value = None
        if value:
            return value
        text = ''
        try:
            text = (self.launch_profile_combo.currentText() or '').strip()
        except Exception:
            text = ''
        return text or None

    def _open_browser(self) -> None:
        if self._launch_worker and self._launch_worker.isRunning():
            InfoBar.warning(
                title=self._t('info_busy_title'),
                content=self._t('info_busy_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return

        launch_profile_id = self._resolve_launch_profile_id()
        effective_profile_id = resolve_effective_profile_id(launch_profile_id, self._current_profile_id)
        if not effective_profile_id:
            InfoBar.warning(
                title=self._t('info_select_profile_title'),
                content=self._t('info_select_profile_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return

        needs_sync = (
            self._current_profile_id != effective_profile_id
            or not self._current_profile
        )
        if needs_sync:
            if launch_profile_id and self._current_profile_id and launch_profile_id != self._current_profile_id:
                InfoBar.info(
                    title=self._t('info_profile_syncing_title'),
                    content=self._t('info_profile_syncing_body'),
                    parent=self,
                    position=InfoBarPosition.TOP,
                )
            profile = load_profile(effective_profile_id)
            self._set_profile_details(effective_profile_id, profile)
            if not profile:
                InfoBar.error(
                    title=self._t('info_profile_invalid_title'),
                    content=self._t('info_profile_invalid_body').format(profile_id=effective_profile_id),
                    parent=self,
                    position=InfoBarPosition.TOP,
                )
                return

        if not self._current_profile_id or not self._current_profile:
            InfoBar.warning(
                title=self._t('info_profile_invalid_title'),
                content=self._t('info_profile_invalid_body').format(profile_id=self._current_profile_id or ''),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return

        url = self.url_input.text().strip() or 'https://example.com'
        self.open_btn.setEnabled(False)
        InfoBar.info(
            title=self._t('info_launching_title'),
            content=self._t('info_launching_body'),
            parent=self,
            position=InfoBarPosition.TOP,
        )

        browser_path = None
        try:
            adapter_id = self._current_profile.base_config.adapter_id
        except Exception:
            adapter_id = 'chromium'

        if adapter_id == 'chromium':
            browser_path = self._resolve_browser_path(self._current_profile)
        self._log_settings(f'Launch browser path: {browser_path}')
        self._launch_worker = BrowserLaunchWorker(
            self._current_profile_id, self._current_profile, url, browser_path
        )
        self._launch_worker.finished.connect(self._on_browser_launched)
        self._launch_worker.start()

    def _on_browser_launched(self, success: bool, message: str) -> None:
        self.open_btn.setEnabled(True)
        if success and self._launch_worker and self._launch_worker.page:
            self._pages.append(self._launch_worker.page)
            InfoBar.success(
                title=self._t('info_launched_title'),
                content=self._t('info_launched_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
        else:
            if message:
                InfoBar.error(
                    title=self._t('info_launch_failed_title'),
                    content=message or self._t('info_launch_failed_body'),
                    parent=self,
                    position=InfoBarPosition.TOP,
                )
