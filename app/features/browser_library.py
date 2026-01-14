from pathlib import Path
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets
from qfluentwidgets import InfoBar, InfoBarPosition, MessageBox, RoundMenu

from app.browser_library import load_browser_library, remove_local_browser
from app.profile_utils import list_profile_entries
from spoofers.profile import load_profile


class BrowserLibraryMixin:
    def refresh_browser_library(self) -> None:
        self._browser_entries = load_browser_library()
        self.browser_library_list.clear()
        for entry in self._browser_entries:
            label = f'{entry.name} {entry.version} ({entry.source})'
            item = QtWidgets.QListWidgetItem(label)
            item.setToolTip(str(entry.path))
            item.setData(QtCore.Qt.ItemDataRole.UserRole, entry.id)
            self.browser_library_list.addItem(item)
        self._populate_profile_browser_combo(
            self._current_profile.base_config.browser_path if self._current_profile else None
        )

    def _show_browser_library_menu(self, position: QtCore.QPoint) -> None:
        item = self.browser_library_list.itemAt(position)
        if not item:
            return
        self.browser_library_list.setCurrentItem(item)
        entry_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
        entry = self._find_browser_entry(entry_id)
        if not entry:
            return
        menu = RoundMenu(parent=self)
        details_action = QtGui.QAction(self._t('browser_library_menu_details'), self)
        menu.addAction(details_action)
        details_action.triggered.connect(lambda checked=False, e=entry: self._show_browser_details(e))
        if entry.source == 'local':
            uninstall_action = QtGui.QAction(self._t('browser_library_menu_uninstall'), self)
            menu.addAction(uninstall_action)
            uninstall_action.triggered.connect(
                lambda checked=False, e=entry: self._uninstall_local_browser(e)
            )
        menu.exec(self.browser_library_list.mapToGlobal(position))

    def _find_browser_entry(self, entry_id: Optional[str]) -> Optional[object]:
        if not entry_id:
            return None
        for entry in self._browser_entries:
            if entry.id == entry_id:
                return entry
        return None

    def _browser_label(self, browser_id: Optional[str]) -> str:
        if not browser_id:
            return ''
        for entry in self._browser_entries:
            if entry.id == browser_id or str(entry.path) == browser_id:
                return f'{entry.name} {entry.version} ({entry.source})'
        return str(browser_id)

    def _format_browser_details(self, entry, verbose: bool) -> str:
        lines = [
            f"{self._t('browser_detail_name')}: {entry.name}",
            f"{self._t('browser_detail_version')}: {entry.version}",
            f"{self._t('browser_detail_source')}: {entry.source}",
        ]
        if verbose:
            lines.append(f"{self._t('browser_detail_path')}: {entry.path}")
            lines.append(f"{self._t('browser_detail_id')}: {entry.id}")
        return '\n'.join(lines)

    def _show_browser_details(self, entry) -> None:
        verbose = entry.source == 'local'
        title_key = 'browser_detail_title_local' if verbose else 'browser_detail_title'
        dialog = MessageBox(
            self._t(title_key),
            self._format_browser_details(entry, verbose),
            self,
        )
        dialog.cancelButton.hide()
        dialog.exec()

    def _normalize_browser_id(self, browser_id: Optional[str]) -> Optional[str]:
        if not browser_id:
            return None
        try:
            return str(Path(browser_id).resolve())
        except Exception:
            return browser_id

    def _profiles_using_browser(self, browser_id: str) -> list[str]:
        normalized = self._normalize_browser_id(browser_id)
        used_by = []
        for entry in list_profile_entries():
            profile = load_profile(entry['id'])
            if not profile or not profile.base_config.browser_path:
                continue
            if self._normalize_browser_id(profile.base_config.browser_path) == normalized:
                used_by.append(entry['id'])
        return used_by

    def _uninstall_local_browser(self, entry) -> None:
        used_by = self._profiles_using_browser(entry.id)
        if used_by:
            dialog = MessageBox(
                self._t('browser_library_uninstall_in_use_title'),
                self._t('browser_library_uninstall_in_use_body').format(
                    profiles=', '.join(used_by)
                ),
                self,
            )
            dialog.cancelButton.hide()
            dialog.exec()
            return
        dialog = MessageBox(
            self._t('browser_library_uninstall_title'),
            self._t('browser_library_uninstall_body').format(
                name=entry.name,
                version=entry.version,
            ),
            self,
        )
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        try:
            remove_local_browser(entry)
        except Exception as exc:
            self._log(f'Uninstall failed: {exc}')
            InfoBar.error(
                title=self._t('browser_library_uninstall_failed_title'),
                content=self._t('browser_library_uninstall_failed_body'),
                parent=self,
                position=InfoBarPosition.TOP,
            )
            return
        InfoBar.success(
            title=self._t('browser_library_uninstall_success_title'),
            content=self._t('browser_library_uninstall_success_body'),
            parent=self,
            position=InfoBarPosition.TOP,
        )
        self.refresh_browser_library()

    def _resolve_browser_path(self, profile) -> Optional[str]:
        browser_path = None
        try:
            browser_path = profile.base_config.browser_path
        except Exception:
            browser_path = getattr(profile, 'browser_id', None)

        if browser_path:
            try:
                if Path(str(browser_path)).exists():
                    return str(browser_path)
            except Exception:
                pass
            for entry in self._browser_entries:
                if entry.id == browser_path or str(entry.path) == browser_path:
                    return str(entry.path)
        if self._browser_entries:
            return str(self._browser_entries[0].path)
        return None
